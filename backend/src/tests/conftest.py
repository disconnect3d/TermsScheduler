import base64

import pytest

from application import create_app
from application import db as alchemy_db
from application.models import User, Group, Subject


@pytest.fixture
def app():
    return create_app('../test_config.py')


@pytest.yield_fixture
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
    def _create_user(username, password, is_admin, groups=None):
        if not groups:
            groups = []

        u = User(username=username, email='test@test.test', first_name='first_name', last_name='last_name',
                 is_admin=is_admin, groups=groups)
        u.hash_password(password)

        db.session.add(u)
        db.session.commit()

        return u

    return _create_user


@pytest.fixture
def user1(create_user):
    """
    Creates test_user:test_password user account.
    """
    return create_user('user1', 'password1', is_admin=False)


@pytest.fixture
def user2(create_user):
    """
    Creates test_user:test_password user account.
    """
    return create_user('user2', 'password2', is_admin=False)


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
def user1_with_1_group(user1, groups, db):
    user1.groups.extend(groups[:1])
    db.session.add(user1)
    db.session.commit()
    return user1


@pytest.fixture
def user1_with_2_groups(user1, groups, db):
    user1.groups.extend(groups[:2])
    db.session.add(user1)
    db.session.commit()
    return user1


def calc_auth_header_value(user, pwd):
    # basic auth uses base64 user:pass
    encoded = base64.b64encode(bytes('{}:{}'.format(user, pwd).encode('utf-8'))).decode('utf-8')
    return 'Authorization', "Basic {}".format(encoded)


@pytest.fixture
def auth_header1(user1):
    """
    Returns Authorization header for the `user1` account using its auth token.
    """
    token = user1.generate_auth_token(600).decode('ascii')
    return calc_auth_header_value(token, 'unused field - can be anything')


@pytest.fixture
def admin_auth_header(admin):
    """
    Returns Authorization header for the test_admin:test_password account using its auth token.
    """
    token = admin.generate_auth_token(600).decode('ascii')
    return calc_auth_header_value(token, 'unused field - can be anything')


@pytest.fixture
def subjects(db, groups):
    """
    Creates subjects and assigns them to groups:
    - group1: sub1, sub2, sub3
    - group2: sub4, sub5, sub6
    - group3: sub1, sub2, sub3, sub4, sub5

    Returns created subjects.
    """
    group1, group2, group3 = groups

    subjects = (
        Subject(name='sub1', groups=[group1, group3]),
        Subject(name='sub2', groups=[group1, group3]),
        Subject(name='sub3', groups=[group1, group3]),
        Subject(name='sub4', groups=[group2, group3]),
        Subject(name='sub5', groups=[group2, group3]),
        Subject(name='sub6', groups=[]),
    )

    for subject in subjects:
        db.session.add(subject)
    db.session.commit()

    return subjects
