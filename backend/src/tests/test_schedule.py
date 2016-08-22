import pytest
from flask import url_for

from application.models import Subject


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


@pytest.fixture(scope='session')
def url_get_subjects():
    return url_for('subjectlist')


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


def test_get_subjects_as_user_with_no_groups(url_get_subjects, subjects, valid_admin_auth_header, client):
    res = client.get(url_get_subjects, headers=[valid_admin_auth_header])

    assert res.status_code == 200
    assert res.json == {'subjects': []}


def test_get_subjects_as_user_with_2_groups(url_get_subjects, subjects, user_with_2_groups, valid_auth_header, client):
    res = client.get(url_get_subjects, headers=[valid_auth_header])

    assert res.status_code == 200
    assert res.json == {
        'subjects': [subject_dict(i) for i in range(1, 6)]
    }
