from flask import json
from flask import request, jsonify, url_for, g, Blueprint
from flask.ext.restful import abort, Resource, reqparse

from application import db
from application.decorators import public_endpoint, require_admin
from application.models import User, Group, Subject, SubjectSignup
from sqlalchemy import func

bp = Blueprint('api', __name__)


@bp.route('/api/login')
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


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
            print("Abort - user already exists.")
            abort(400)  # existing user

        # TODO / FIXME: email validation ...
        user = User(username=args.username, first_name=args.first_name, last_name=args.last_name, email=args.email)
        user.hash_password(args.password)
        db.session.add(user)
        db.session.commit()
        return {'username': user.username}, 201, {'Location': url_for('userresource', id=user.id, _external=True)}


class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)

        if not user:
            abort(400)

        return {'username': user.username}


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
        user_group_ids = [i.id for i in g.user.groups]
        subjects = list(User.get_subjects(user_group_ids))

        return jsonify({'subjects': subjects})


subject_signup_parser = reqparse.RequestParser(bundle_errors=True)
subject_signup_parser.add_argument('subject_id', type=int, required=True)


class SubjectSignupList(Resource):
    def get(self):
        ss = list(SubjectSignup.query.filter(SubjectSignup.user_id == g.user.id).join(Subject).order_by(Subject.name))
        return jsonify({'subjects_signup': ss})

    def post(self):
        args = subject_signup_parser.parse_args(strict=True)

        if User.has_subject(g.user.id, args.subject_id):
            signed, = db.session.query(
                func.count(SubjectSignup.subject_id)
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
        if User.has_subject(g.user.id, subject_id):
            SubjectSignup.query.filter(subject_id=subject_id, user_id=g.user.id).delete()
            db.session.commit()
            return {}

        abort(400, message="Can't delete subject you are not signed on.")
