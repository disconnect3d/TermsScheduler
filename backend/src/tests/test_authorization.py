import json

import pytest
from flask import url_for
from flask.ext.restful import Resource, Api

from application.decorators import public_endpoint, require_admin
from application.models import Group
from tests.conftest import calc_auth_header_value


@pytest.fixture
def url_require_admin(app):
    @app.route('/api/test_require_admin')
    @require_admin
    def endpoint_require_admin():
        return '', 200

    return url_for('endpoint_require_admin')


@pytest.fixture(scope='session')
def url_get_auth_token():
    return url_for('api.get_auth_token')


@pytest.fixture(scope='session')
def url_grouplist():
    return url_for('grouplist')


@pytest.fixture(scope='session')
def url_userlist():
    return url_for('userlist')


def test_app_endpoints_require_login(app, db, client):
    @app.route('/api/test_require_login')
    def endpoint_require_login():
        return '', 200

    assert client.get(url_for('endpoint_require_login')).status_code == 401


def test_app_public_endpoint(app, client):
    @public_endpoint
    @app.route('/api/test_public_endpoint')
    def endpoint_public():
        return '', 200

    assert client.get(url_for('endpoint_public')).status_code == 200


def test_app_public_endpoint_resource(app, client):
    class RestResource(Resource):
        @public_endpoint
        def get(self):
            return {}

    api = Api(app)
    api.add_resource(RestResource, '/test_restresource_url')

    assert client.get(url_for('restresource')).status_code == 200


def test_app_require_admin_unauthorized(url_require_admin, db, client):
    assert client.get(url_require_admin).status_code == 401


def test_app_require_admin_not_an_admin(url_require_admin, auth_header1, client):
    assert client.get(url_require_admin, headers=[auth_header1]).status_code == 401


def test_app_require_admin_authorized(url_require_admin, admin_auth_header, client):
    assert client.get(url_require_admin, headers=[admin_auth_header]).status_code == 200


def test_create_user_missing_params(url_userlist, db, client):
    missing = 'Missing required parameter in the JSON body or the post body or the query string'
    params = ('username', 'password', 'first_name', 'last_name', 'email')

    res = client.post(url_userlist, data=json.dumps({}), content_type='application/json')
    assert res.status_code == 400
    assert res.json == {'message': {p: missing for p in params}}


def test_create_user(url_userlist, db, client):
    data = {
        'username': 'test_create_user_user',
        'password': 'test_create_user_user',
        'first_name': 'test_create_user_user',
        'last_name': 'test_create_user_user',
        'email': 'email@email.email'
    }

    res = client.post(url_userlist, data=json.dumps(data), content_type='application/json')
    assert res.status_code == 201
    assert res.headers.get('Location').endswith('/api/users/1') == True


def test_get_user_unauthorized(db, client):
    res = client.get(url_for('userresource', id=1))
    assert res.status_code == 401


def test_get_user_authorized(auth_header1, db, client):
    res = client.get(url_for('userresource', id=1),  headers=[auth_header1])
    assert res.status_code == 200
    assert res.json == {'username': 'user1'}


def test_login_no_credentials_unauthorized(url_get_auth_token, db, client):
    res = client.get(url_get_auth_token)
    assert res.status_code == 401


def test_login_bad_password_unauthorized(url_get_auth_token, user1, client):
    invalid_auth = calc_auth_header_value('test_user', 'test_wrong_password')

    res = client.get(url_get_auth_token, headers=[invalid_auth])
    assert res.status_code == 401


def test_login_authorized_by_token(url_get_auth_token, auth_header1, user1, client):
    res = client.get(url_get_auth_token, headers=[auth_header1])

    assert res.status_code == 200
    assert set(res.json.keys()) == {'duration', 'token'}
    assert res.json['token'] == user1.generate_auth_token(600).decode('ascii')
    assert res.json['duration'] == 600


def test_login_authorized(url_get_auth_token, user1, client):
    auth_header = calc_auth_header_value('user1', 'password1')
    test_login_authorized_by_token(url_get_auth_token, auth_header, user1, client)


def test_get_groups_user_with_no_groups(url_grouplist, groups, auth_header1, client):
    res = client.get(url_grouplist, headers=[auth_header1])

    assert res.status_code == 200
    assert res.json == {u'groups': []}


def test_get_groups_user_with_groups(url_grouplist, user1_with_2_groups, auth_header1, client):
    res = client.get(url_grouplist, headers=[auth_header1])

    assert res.status_code == 200
    assert res.json == {u'groups': [u'group1', u'group2']}


def test_new_group_require_admin(url_grouplist, auth_header1, client):
    res = client.post(url_grouplist, headers=[auth_header1],
                      data=json.dumps({'name': 'test_group'}),
                      content_type='application/json')
    assert res.status_code == 401


def test_new_group_create(url_grouplist, admin_auth_header, db, client):
    group_name = 'test_group'

    assert Group.query.count() == 0

    res = client.post(url_grouplist, headers=[admin_auth_header],
                      data=json.dumps({'name': group_name}),
                      content_type='application/json')

    assert res.status_code == 201
    assert res.json == {}

    groups = Group.query.all()
    assert len(groups) == 1
    assert groups[0].name == group_name
