import pytest
from flask import json
from flask import url_for

from application.models import SubjectSignup, Setting
from tests.conftest import calc_auth_header_value


@pytest.fixture
def create_subject_signup_for_user(db):
    def _create_subject_signup_for_user(user_id, subject_ids):
        for subject_id in subject_ids:
            db.session.add(SubjectSignup(subject_id=subject_id, user_id=user_id))

        db.session.commit()

    return _create_subject_signup_for_user


@pytest.fixture
def user2_with_subject_signups(user2, subjects, db):
    subjects_signup = (
        SubjectSignup(subject_id=1, user_id=user2.id),
        SubjectSignup(subject_id=2, user_id=user2.id)
    )

    for ss in subjects_signup:
        db.session.add(ss)
    db.session.commit()


@pytest.fixture
def url_get_subjects(db_settings):
    return url_for('subjectlist')


@pytest.fixture
def url_subjectsignup(db_settings):
    return url_for('subjectsignuplist')


def subject_dict(i):
    # Yes, no `groups` returned here
    return {
        'name': 'sub%d' % i,
        'description': '',
        'ects': 0,
        'exercises_hours': 0,
        'id': i,
        'lab_hours': 0,
        'lecture_hours': 0,
        'maximum_members': 15,
        'minimum_members': 5,
        'project_hours': 0,
        'seminar_hours': 0,
        'syllabus_url': ''
    }


def test_get_subjects_unauthorized(url_get_subjects, db, client):
    res = client.get(url_get_subjects)

    assert res.status_code == 401


def test_get_subjects_as_user_with_no_groups(url_get_subjects, subjects, admin_auth_header, client):
    res = client.get(url_get_subjects, headers=[admin_auth_header])

    assert res.status_code == 200
    assert res.json == {'subjects': []}


def test_get_subjects_as_user_with_2_groups(url_get_subjects, subjects, user1_with_2_groups, auth_header1, client):
    res = client.get(url_get_subjects, headers=[auth_header1])

    assert res.status_code == 200
    assert res.json == {
        'subjects': [subject_dict(i) for i in range(1, 6)]
    }


def test_get_subjects_signup_unauthorized(url_subjectsignup, db, client):
    res = client.get(url_subjectsignup)

    assert res.status_code == 401


def test_get_subjects_signup_as_user_with_no_groups(url_subjectsignup, subjects, admin_auth_header, client):
    res = client.get(url_subjectsignup, headers=[admin_auth_header])

    assert res.status_code == 200
    assert res.json == {'subjects_signup': []}


def test_get_subjects_signup_as_user_with_2_subjects_signed(url_subjectsignup, create_subject_signup_for_user, user1,
                                                            user2, auth_header1, subjects, client):
    create_subject_signup_for_user(user_id=1, subject_ids=[1, 2])
    create_subject_signup_for_user(user_id=2, subject_ids=[3, 4])

    res = client.get(url_subjectsignup, headers=[auth_header1])

    assert res.status_code == 200
    assert res.json == {'subjects_signup': [
        {'subject_id': 1, 'user_id': 1},
        {'subject_id': 2, 'user_id': 1},
    ]}


def test_post_subject_signup_unauthorized(url_subjectsignup, db, client):
    res = client.post(url_subjectsignup, data=json.dumps({'subject_id': 1}), content_type='application/json')

    assert res.status_code == 401


def test_post_subject_signup_user_without_groups(url_subjectsignup, admin_auth_header, subjects, client):
    res = client.post(url_subjectsignup, data=json.dumps({'subject_id': 1}), headers=[admin_auth_header],
                      content_type='application/json')

    assert res.status_code == 400
    assert res.json == {'message': "You can't signup for subject 1."}


def test_post_subject_signup_user_with_groups(url_subjectsignup, auth_header1, user1_with_2_groups, subjects, client):
    res = client.post(url_subjectsignup, data=json.dumps({'subject_id': 1}), headers=[auth_header1],
                      content_type='application/json')

    assert res.status_code == 200
    assert res.json == {'signed': {'subject_id': 1, 'user_id': 1}}


def test_post_subject_signup_disabled_signup(url_subjectsignup, auth_header1, user1_with_2_groups, subjects, db, client):
    db.session.query(Setting). \
        filter(Setting.name == Setting.SUBJECTS_SIGNUP). \
        update({Setting.value: '0'})
    db.session.commit()

    res = client.post(url_subjectsignup, data=json.dumps({'subject_id': 1}), headers=[auth_header1],
                      content_type='application/json')

    assert res.status_code == 400
    assert res.json == {'message': "Can't enroll on subject - signup is disabled."}


def test_post_subject_signup_user_with_groups_no_space_for_subject(
        url_subjectsignup, create_user, groups, subjects, client):
    group1, *_ = groups

    def signup_user_id(id_):
        login_pwd = 'user%d' % id_
        create_user(login_pwd, login_pwd, is_admin=False, groups=[group1])
        header = calc_auth_header_value(login_pwd, login_pwd)

        return client.post(url_subjectsignup, data=json.dumps({'subject_id': 1}), headers=[header],
                           content_type='application/json')

    for i in range(1, 16):
        res = signup_user_id(i)
        assert res.status_code == 200
        assert res.json == {'signed': {'subject_id': 1, 'user_id': i}}

    res = signup_user_id(16)
    assert res.status_code == 400
    assert res.json == {'message': 'There is no space left on subject 1.'}


def test_delete_subject_signup_unauthorized(db, client):
    res = client.delete(url_for('subjectsignupresource', subject_id=1))

    assert res.status_code == 401


def test_delete_subject_signup_doesnt_exist(db, auth_header1, client):
    res = client.delete(url_for('subjectsignupresource', subject_id=1), headers=[auth_header1])

    assert res.status_code == 400
    assert res.json == {'message': "Can't delete subject you are not signed on."}


def test_delete_subject_signup_deleted(create_subject_signup_for_user, auth_header1, subjects, db, client):
    create_subject_signup_for_user(user_id=1, subject_ids=[1])

    res = client.delete(url_for('subjectsignupresource', subject_id=1), headers=[auth_header1])

    assert res.status_code == 400
    assert res.json == {'message': "Can't delete subject you are not signed on."}
