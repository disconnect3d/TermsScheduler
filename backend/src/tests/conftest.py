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
def create_user(db):
    def _create_user(username, password, is_admin):
        u = User(username=username, email='test@test.test', first_name='first_name', last_name='last_name',
                 is_admin=is_admin)
        u.hash_password(password)

        db.session.add(u)
        db.session.commit()

        return u

    return _create_user


@pytest.fixture
def user(create_user):
    """
    Creates test_user:test_password user account.
    """
    return create_user('test_user', 'test_password', is_admin=False)


@pytest.fixture
def admin(create_user):
    """
    Creates test_admin:test_password user account.
    """
    return create_user('test_admin', 'test_password', is_admin=True)


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


def calc_auth_header_value(user, pwd):
    # basic auth uses base64 user:pass
    return "Basic {}".format(base64.b64encode(bytes('{}:{}'.format(user, pwd).encode('utf-8'))).decode('utf-8'))


@pytest.fixture
def valid_auth_header(user):
    """
    Returns Authorization header for the test_user:test_password account using its auth token.
    """
    token = user.generate_auth_token(600).decode('ascii')
    return 'Authorization', calc_auth_header_value(token, 'unused field - can be anything')


@pytest.fixture
def valid_admin_auth_header(admin):
    """
    Returns Authorization header for the test_admin:test_password account using its auth token.
    """
    token = admin.generate_auth_token(600).decode('ascii')
    return 'Authorization', calc_auth_header_value(token, 'unused field - can be anything')
