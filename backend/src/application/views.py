from flask import current_app as app
from flask import request, jsonify, g, Blueprint
from flask.ext.restful import abort, Resource, reqparse
from sqlalchemy import func

from application import db
from application.decorators import public_endpoint, require_admin
from application.models import User, Group, Subject, SubjectSignup, TermSignup, Term, TermGroup, Setting
from application.utils import DefaultOrderedDict

bp = Blueprint('api', __name__)


@bp.route('/api/login')
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({
        'token': token.decode('ascii'),
        'duration': 600,
        'id': g.user.id,
    })


user_parser = reqparse.RequestParser(bundle_errors=True)
user_parser.add_argument('username', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)
user_parser.add_argument('first_name', type=str, required=True)
user_parser.add_argument('last_name', type=str, required=True)
user_parser.add_argument('email', type=str, required=True)


class UserList(Resource):
    @public_endpoint
    def post(self):
        args = user_parser.parse_args(strict=True)

        if User.query.filter_by(username=args.username).first() is not None:
            abort(400, message="User already exists")

        # TODO / FIXME: email validation ...
        user = User(username=args.username, first_name=args.first_name, last_name=args.last_name, email=args.email)
        user.hash_password(args.password)
        db.session.add(user)
        db.session.commit()
        return 201


class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)

        if not user:
            abort(400)
        response = {c.name: getattr(user, c.name) for c in User.__table__.columns}
        response.pop('is_admin')
        response.pop('password_hash')
        return response


class GroupList(Resource):
    def get(self):
        return jsonify({'groups': [grp.name for grp in g.user.groups]})

    @require_admin
    def post(self):
        name = request.get_json()['name']

        db.session.add(Group(name=name))
        db.session.commit()

        return {}, 201


class SubjectList(Resource):
    def get(self):
        """
        :return: List of subjects that can be chosen by particular user.
        """
        return jsonify({'subjects': list(g.user.get_subjects())})


subject_signup_parser = reqparse.RequestParser(bundle_errors=True)
subject_signup_parser.add_argument('subject_id', type=int, required=True)


class SubjectSignupList(Resource):
    def get(self):
        ss = list(SubjectSignup.query.filter(SubjectSignup.user_id == g.user.id).join(Subject).order_by(Subject.name))
        return jsonify({'subjects_signup': ss})

    def post(self):
        opts = Setting.get_from_db()
        if not opts.SUBJECTS_SIGNUP:
            abort(400, message="Can't enroll on subject - signup is disabled.")

        args = subject_signup_parser.parse_args(strict=True)

        if g.user.has_subject(args.subject_id):
            signed, = db.session.query(
                func.count(SubjectSignup.user_id)
            ).filter(SubjectSignup.subject_id == args.subject_id).first()

            limit, = db.session.query(Subject.maximum_members).filter(Subject.id == args.subject_id).first()

            if signed < limit:
                ss = SubjectSignup(subject_id=args.subject_id, user_id=g.user.id)
                db.session.add(ss)
                db.session.commit()
                return jsonify({'signed': ss})

            abort(400, message="There is no space left on subject %d." % args.subject_id)

        abort(400, message="You can't signup for subject %d." % args.subject_id)


class SubjectSignupResource(Resource):
    def delete(self, subject_id):
        #opts = Setting.get_from_db()
        # if not opts.SUBJECTS_SIGNUP:
        #     abort(400, message="Can't drop from subject - signup is disabled.")

        if g.user.has_subject(subject_id):
            SubjectSignup.query.filter(SubjectSignup.subject_id == subject_id,
                                       SubjectSignup.user_id == g.user.id).delete(synchronize_session=False)
            db.session.expire_all()
            db.session.commit()
            return {}

        abort(400, message="Can't delete subject you are not signed on.")


class SettingList(Resource):
    def get(self):
        settings = Setting.query.filter(Setting.name.in_(app.config['SETTINGS_IN_DB'])).order_by(Setting.name)
        return jsonify({'settings': list(settings)})


class TermSignupAction(Resource):
    def get(self):
        """
        Returns json in form:
        {
            'subject_terms': [
                {
                    "subject_name": "math",
                    "terms_aggregated": [
                        {
                            'term_type': 'Exercises',
                            'terms': [ ... ]
                        }
                    ]
                },
                ...
            ]
        }
        """
        fields = (
            Subject.name, Term.type, Term.id, Term.day, Term.time_from, Term.time_to,
            TermSignup.points, TermSignup.reason, TermSignup.reason_accepted
        )

        res = db.session.query(*fields) \
            .join(Term) \
            .join(TermGroup) \
            .outerjoin(TermSignup) \
            .filter(TermGroup.group_id.in_([i.id for i in g.user.groups])) \
            .order_by(Subject.name, Term.day, Term.time_from)

        subjects_terms = DefaultOrderedDict(lambda: DefaultOrderedDict(lambda: []))

        for record in res:
            subject_name, term_type, *term_data = record

            term_data = dict(zip(record._fields[2:], record[2:]))

            # If there is no matching TermSignup, set defaults
            if term_data['points'] is None:
                term_data['points'] = 0
                term_data['reason'] = ''
                term_data['reason_accepted'] = False

            subjects_terms[subject_name][term_type].append(term_data)

        subjects_terms_aggregated = [
            {
                'subject_name': subject_name,
                'terms_aggregated': [
                    {
                        'term_type': term_type,
                        'terms': terms
                    }
                ]
            } for subject_name, type_terms_dict in subjects_terms.items()
            for term_type, terms in type_terms_dict.items()
            ]

        return jsonify({'subjects_terms': subjects_terms_aggregated})

    def post(self):
        """
        Expects JSON of form:
        {
            'terms_signup': [
                {
                    'term_id': 1,
                    'points': 5,
                    'reason': 'bla bla bla',    // OR EMPTY STRING
                },
                ...
            ]
        }
        """
        opts = Setting.get_from_db()
        if not opts.TERMS_SIGNUP:
            abort(400, message='Terms signup is disabled.')

        TermSignup.query.filter(TermSignup.user_id == g.user.id).delete()
        db.session.commit()

        # TODO / FIXME : use something better than hand made json validation
        # RequestParser can't really handle nested jsons well, maybe flask-marshmallow?
        terms_signup = []
        term_ids = []
        try:
            j = request.json

            if set(j.keys()) != {'terms_signup'}:
                raise Exception('Invalid json format.')

            for term_signup in j['terms_signup']:
                term_id = term_signup['term_id']
                reason = term_signup['reason']

                ts = TermSignup(
                    term_id=term_id,
                    user_id=g.user.id,
                    points=term_signup['points'] if not reason else 0,
                    reason=reason
                )
                term_ids.append(term_id)
                terms_signup.append(ts)

            if len(term_ids) != len(set(term_ids)):
                raise Exception('Duplicated term_ids.')

        except Exception as e:
            print('Exception while parsing TermSignupAction post JSON: "%s"' % e)
            abort(400, message='Invalid json format.')

        # Checking if the json contains ALL terms user had to set points on
        grps = [i.id for i in g.user.groups]
        expected_term_ids = db.session.query(Term.id).join(TermGroup).filter(TermGroup.group_id.in_(grps))
        expected_term_ids = (i for i, in expected_term_ids)

        if set(term_ids) != set(expected_term_ids):
            abort(400, message='Missing term_ids in terms_signups list.')

        db.session.add_all(terms_signup)
        db.session.commit()
        return {}
