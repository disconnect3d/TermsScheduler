from application import db
from flask import request, jsonify, url_for, g, Blueprint
from flask.ext.restful import abort

from application.authorization.models import User
from application.decorators import public_endpoint


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/login')
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@bp.route('/users', methods=['POST'])
@public_endpoint
def new_user():
    json_data = request.get_json()
    username = json_data.get('username')
    password = json_data.get('password')

    if username is None or password is None:
        print("Abort - username or password is None.")
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        print("Abort - user already exists.")
        abort(400)  # existing user

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('api.get_user', id=user.id, _external=True)})


@bp.route('/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

