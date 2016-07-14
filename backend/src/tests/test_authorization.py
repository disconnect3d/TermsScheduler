import base64

import pytest
from flask import url_for

from application import db as alchemy_db
from application.authorization.models import User


@pytest.yield_fixture(scope='function')
def db(app):
    """
    Creates database before a test and destroys it afterwards.
    """
    _db = alchemy_db
    _db.create_all()
    yield _db
    _db.session.rollback()
    _db.drop_all()


@pytest.fixture
def user(db):
    """
    Creates simple test:test user account.
    """
    u = User(username='test_user', email='test@test.test', first_name='first_name', last_name='last_name')
    u.hash_password('test_password')

    db.session.add(u)
    db.session.commit()


def _auth_method(user, pwd):
    # basic auth uses base64 user:pass
    return "Basic {}".format(base64.b64encode(bytes('{}:{}'.format(user, pwd).encode('utf-8'))).decode('utf-8'))


def test_login_no_credentials_unauthorized(db, client):
    res = client.get(url_for('api.get_auth_token'))
    assert res.status_code == 401


def test_login_bad_password_unauthorized(user, client):
    invalid_auth = _auth_method('test_user', 'test_wrong_password')

    res = client.get(url_for('api.get_auth_token'), headers=[('Authorization', invalid_auth)])
    assert res.status_code == 401


def test_login_authorized(user, client):
    valid_auth = _auth_method('test_user', 'test_password')

    res = client.get(url_for('api.get_auth_token'), headers=[('Authorization', valid_auth)])
    assert res.status_code == 200
    assert set(res.json.keys()) == {'duration', 'token'}
    assert res.json['duration'] == 600
