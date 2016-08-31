from collections import defaultdict

from flask import request, jsonify, g, Blueprint
from flask.ext.restful import abort, Resource, reqparse

from application import db
from application.decorators import public_endpoint, require_admin
from application.models import User, Group, Subject, SubjectSignup, TermSignup, Term, TermGroup
from sqlalchemy import func

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
        if g.user.has_subject(subject_id):
            SubjectSignup.query.filter(SubjectSignup.subject_id == subject_id,
                                       SubjectSignup.user_id == g.user.id).delete(synchronize_session=False)
            db.session.expire_all()
            db.session.commit()
            return {}

        abort(400, message="Can't delete subject you are not signed on.")


class SubjectWithTermList(Resource):
    def get(self):
        """
        :return: List of terms that can be chosen by particular user.
        """
        return jsonify


term_signup_parser = reqparse.RequestParser(bundle_errors=True)
term_signup_parser.add_argument('term_id', type=int, required=True)


class TermList(Resource):
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
        from manage import logsql
        logsql()
        fields = (Subject.name, Term.type, Term.id, Term.day, Term.time_from, Term.time_to)
        res = db.session.query(*fields).join(Term).join(TermGroup) \
            .filter(TermGroup.group_id.in_([i.id for i in g.user.groups])) \
            .order_by(Subject.name, Term.day, Term.time_from)

        subjects_terms = DefaultOrderedDict(lambda: DefaultOrderedDict(lambda: []))

        for record in res:
            subject_name, term_type, *term_data = record
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


class TermSignupList(Resource):
    def get(self):
        ss = list(
            TermSignup.query.filter(TermSignup.user_id == g.user.id).join(Term).order_by(Term.day, Term.time_from))
        return jsonify({'terms_signup': ss})

    def post(self):
        # TODO / FIXME / WIP
        args = term_signup_parser.parse_args(strict=True)

        if g.user.has_term(args.term_id):
            ts = TermSignup(term_id=args.term_id, user_id=g.user.id)
            db.session.add(ts)
            db.session.commit()
            return jsonify({'term_signup': ts})

        abort(400, message="You can't signup for subject %d." % args.subject_id)
