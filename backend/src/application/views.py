from flask import request, jsonify, url_for, g, Blueprint
from flask.ext.restful import abort, Resource, reqparse

from application import db
from application.decorators import public_endpoint, require_admin
from application.models import User, Group, Subject, SubjectSignup

bp = Blueprint('api', __name__)


@bp.route('/api/login')
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('password', type=str)
user_parser.add_argument('first_name', type=str)
user_parser.add_argument('last_name', type=str)


class UserList(Resource):
    @public_endpoint
    def post(self):
        args = user_parser.parse_args(strict=True)
        username, password = args['username'], args['password']
        first_name, last_name = args['firstName'], args['lastName']

        if User.query.filter_by(username=username).first() is not None:
            print("Abort - user already exists.")
            abort(400)  # existing user

        user = User(username=username, first_name=first_name, last_name=last_name)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return {'username': user.username}, 201, {'Location': url_for('api.get_user', id=user.id, _external=True)}


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
        subjects = list(Subject.query.join(Subject.groups).filter(Group.id.in_(user_group_ids)).order_by(Subject.name))

        return jsonify({'subjects': subjects})


class SubjectSignupList(Resource):
    def get(self):
        ss = list(SubjectSignup.query.filter(SubjectSignup.user_id == g.user.id))
        return jsonify({'subjects_signup': ss})

    def post(self):
        pass
