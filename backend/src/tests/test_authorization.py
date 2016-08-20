import json

import pytest
from flask import url_for

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
def url_get_groups():
    return url_for('api.get_groups')


@pytest.fixture(scope='session')
def url_new_group():
    return url_for('api.new_group')


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


def test_app_require_admin_unauthorized(url_require_admin, db, client):
    assert client.get(url_require_admin).status_code == 401


def test_app_require_admin_not_an_admin(url_require_admin, valid_auth_header, client):
    assert client.get(url_require_admin, headers=[valid_auth_header]).status_code == 401


def test_app_require_admin_authorized(url_require_admin, valid_admin_auth_header, client):
    assert client.get(url_require_admin, headers=[valid_admin_auth_header]).status_code == 200


def test_login_no_credentials_unauthorized(url_get_auth_token, db, client):
    res = client.get(url_get_auth_token)
    assert res.status_code == 401


def test_login_bad_password_unauthorized(url_get_auth_token, user, client):
    invalid_auth = calc_auth_header_value('test_user', 'test_wrong_password')

    res = client.get(url_get_auth_token, headers=[('Authorization', invalid_auth)])
    assert res.status_code == 401


def test_login_authorized_by_token(url_get_auth_token, valid_auth_header, user, client):
    res = client.get(url_get_auth_token, headers=[valid_auth_header])

    assert res.status_code == 200
    assert set(res.json.keys()) == {'duration', 'token'}
    assert res.json['token'] == user.generate_auth_token(600).decode('ascii')
    assert res.json['duration'] == 600


def test_login_authorized(url_get_auth_token, user, client):
    valid_auth = calc_auth_header_value('test_user', 'test_password')
    test_login_authorized_by_token(url_get_auth_token, ('Authorization', valid_auth), user, client)


def test_get_groups_user_with_no_groups(url_get_groups, groups, valid_auth_header, client):
    res = client.get(url_get_groups, headers=[valid_auth_header])

    assert res.status_code == 200
    assert res.json == {u'groups': []}


def test_get_groups_user_with_groups(url_get_groups, user_with_2_groups, valid_auth_header, client):
    res = client.get(url_get_groups, headers=[valid_auth_header])

    assert res.status_code == 200
    assert res.json == {u'groups': [u'group1', u'group2']}


def test_new_group_require_admin(url_new_group, valid_auth_header, client):
    res = client.post(url_new_group, headers=[valid_auth_header],
                      data=json.dumps({'name': 'test_group'}),
                      content_type='application/json')
    assert res.status_code == 401


def test_new_group_create(url_new_group, valid_admin_auth_header, db, client):
    group_name = 'test_group'

    assert Group.query.count() == 0

    res = client.post(url_new_group, headers=[valid_admin_auth_header],
                      data=json.dumps({'name': group_name}),
                      content_type='application/json')

    assert res.status_code == 201
    assert res.data == b''

    groups = Group.query.all()
    assert len(groups) == 1
    assert groups[0].name == group_name
