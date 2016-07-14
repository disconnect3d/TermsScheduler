import base64

import pytest

from application import create_app
from application import db as alchemy_db
from application.authorization.models import User, Group


@pytest.fixture
def app():
    return create_app('../test_config.py')


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
    return u


@pytest.fixture
def groups(db):
    """
    Creates `group1`, `group2` and `group3` groups.
    """
    for name in ('group1', 'group2', 'group3'):
        db.session.add(Group(name=name))
    db.session.commit()

    return Group.query.all()


@pytest.fixture
def user_with_2_groups(user, groups, db):
    user.groups.extend(groups[:2])
    db.session.add(user)
    db.session.commit()
    return user


def _auth_method(user, pwd):
    # basic auth uses base64 user:pass
    return "Basic {}".format(base64.b64encode(bytes('{}:{}'.format(user, pwd).encode('utf-8'))).decode('utf-8'))


@pytest.fixture
def valid_auth_header(user):
    """
    Returns Authorization header for the test:test account using its auth token.
    """
    token = user.generate_auth_token(600)
    return 'Authorization', _auth_method(token, 'unused field - can be anything')
