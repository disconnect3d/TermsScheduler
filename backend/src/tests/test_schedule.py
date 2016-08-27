import pytest
from flask import json
from flask import url_for

from application.models import Subject, SubjectSignup


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


@pytest.fixture(scope='session')
def url_get_subjects():
    return url_for('subjectlist')


@pytest.fixture(scope='session')
def url_subjectsignup():
    return url_for('subjectsignuplist')


def subject_dict(i):
    # Yes, no `groups` returned here
    return {
        'name': 'sub%d' % i,
        'description': '',
        'ects': 0,
        'exercises_hours': 0,
        'groups': None,
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


def test_get_subjects_signup_as_user_with_2_subjects_signed(url_subjectsignup, create_subject_signup_for_user, user1, user2, auth_header1, subjects, client):
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
    res = client.post(url_subjectsignup, data=json.dumps({'subject_id': 1}), headers=[admin_auth_header], content_type='application/json')

    assert res.status_code == 400
    assert res.json == {'message': "You can't signup for subject 1."}
