import pytest
from flask import url_for

from application.schedule.models import Subject


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


def test_get_subjects_as_admin(user_with_2_groups, valid_auth_header, client):
    res = client.get(url_for('api.get_groups'), headers=[valid_auth_header])

    assert res.status_code == 200
    assert res.json == {u'groups': [u'group1', u'group2']}

