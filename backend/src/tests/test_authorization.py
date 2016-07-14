from flask import url_for

from tests.conftest import _auth_method


def test_app_endpoints_require_login(app, db, client):
    @app.route('/api/test_require_login')
    def test_require_login():
        pass

    assert client.get(url_for('test_require_login')).status_code == 401


def test_login_no_credentials_unauthorized(db, client):
    res = client.get(url_for('api.get_auth_token'))
    assert res.status_code == 401


def test_login_bad_password_unauthorized(user, client):
    invalid_auth = _auth_method('test_user', 'test_wrong_password')

    res = client.get(url_for('api.get_auth_token'), headers=[('Authorization', invalid_auth)])
    assert res.status_code == 401


def test_login_authorized_by_token(valid_auth_header, user, client):
    res = client.get(url_for('api.get_auth_token'), headers=[valid_auth_header])

    assert res.status_code == 200
    assert set(res.json.keys()) == {'duration', 'token'}
    assert res.json['token'] == user.generate_auth_token(600)
    assert res.json['duration'] == 600


def test_login_authorized(user, client):
    valid_auth = _auth_method('test_user', 'test_password')
    test_login_authorized_by_token(('Authorization', valid_auth), user, client)


def test_get_groups_user_with_no_groups(groups, valid_auth_header, client):
    res = client.get(url_for('api.get_groups'), headers=[valid_auth_header])

    assert res.status_code == 200
    assert res.json == {u'groups': []}


def test_get_groups_user_with_groups(user_with_2_groups, valid_auth_header, client):
    res = client.get(url_for('api.get_groups'), headers=[valid_auth_header])

    assert res.status_code == 200
    assert res.json == {u'groups': [u'group1', u'group2']}
