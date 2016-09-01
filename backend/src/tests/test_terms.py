from datetime import time
import pytest
from flask import json
from flask import url_for

from application.enums import TermType, Day
from application.models import Subject, SubjectSignup, Term, TermSignup


@pytest.fixture
def terms(db, subjects, groups):
    """
    Creates subjects and assigns them to groups:
    - group1: sub1, sub2, sub3
    - group2: sub4, sub5, sub6
    - group3: sub1, sub2, sub3, sub4, sub5

    Returns created subjects.
    """
    group1, group2, group3 = groups

    terms = (
        Term(subject_id=1, type=TermType.lab, day=Day.monday, time_from=time(8, 30), time_to=time(10, 0),
             groups=[group1, group3]),
        Term(subject_id=1, type=TermType.lab, day=Day.tuesday, time_from=time(9, 30), time_to=time(11, 0),
             groups=[group1, group3]),
        Term(subject_id=1, type=TermType.lab, day=Day.wednesday, time_from=time(8, 30), time_to=time(10, 0),
             groups=[group1, group3]),

        Term(subject_id=2, type=TermType.lab, day=Day.friday, time_from=time(8, 30), time_to=time(10, 0),
             groups=[group2]),

        Term(subject_id=3, type=TermType.lab, day=Day.tuesday, time_from=time(19, 0), time_to=time(21, 0),
             groups=[group1, group2]),
        Term(subject_id=3, type=TermType.lab, day=Day.thursday, time_from=time(11, 0), time_to=time(12, 30),
             groups=[group2]),
    )

    for term in terms:
        db.session.add(term)
    db.session.commit()

    return terms


@pytest.fixture(scope='session')
def url_termsignup():
    return url_for('termsignupaction')


def test_get_terms_for_user_unauthorized(url_termsignup, terms, db, client):
    res = client.get(url_termsignup)

    assert res.status_code == 401


def test_get_terms_for_user_no_groups(url_termsignup, terms, db, auth_header1, client):
    res = client.get(url_termsignup, headers=[auth_header1])

    assert res.status_code == 200
    assert res.json == {'subjects_terms': []}


def test_get_terms_for_user_with_groups(url_termsignup, terms, db, auth_header1, user1_with_1_group, client):
    res = client.get(url_termsignup, headers=[auth_header1])

    assert res.status_code == 200
    assert res.json == {
        'subjects_terms': [
            {
                'subject_name': 'sub1',
                'terms_aggregated': [
                    {
                        'term_type': 'Laboratory',
                        'terms': [
                            {'id': 1, 'day': 'Monday', 'time_from': '08:30', 'time_to': '10:00',
                             'points': 0, 'reason': '', 'reason_accepted': False},
                            {'id': 2, 'day': 'Tuesday', 'time_from': '09:30', 'time_to': '11:00',
                             'points': 0, 'reason': '', 'reason_accepted': False},
                            {'id': 3, 'day': 'Wednesday', 'time_from': '08:30', 'time_to': '10:00',
                             'points': 0, 'reason': '', 'reason_accepted': False}
                        ]
                    }
                ]
            },
            {
                'subject_name': 'sub3',
                'terms_aggregated': [
                    {
                        'term_type': 'Laboratory',
                        'terms': [
                            {'id': 5, 'day': 'Tuesday', 'time_from': '19:00', 'time_to': '21:00',
                             'points': 0, 'reason': '', 'reason_accepted': False}
                        ]
                    }
                ]
            }
        ]
    }


def test_post_terms_for_user_with_groups_missing_terms(
        url_termsignup, terms, db, auth_header1, user1_with_1_group, client):
    terms_signup = {
        'terms_signup': [
            {
                'term_id': 1,
                'points': 5,
                'reason': 'bla bla bla',  # // OR EMPTY STRING
            }
        ]
    }

    res = client.post(url_termsignup, headers=[auth_header1], data=json.dumps(terms_signup),
                      content_type='application/json')

    assert res.status_code == 400
    assert res.json == {'message': 'Missing term_ids in terms_signups list.'}


def test_post_terms_for_user_with_groups_all_terms(url_termsignup, terms, db, auth_header1, user1_with_1_group, client):
    terms_signup_json = {
        'terms_signup': [
            {
                'term_id': 1,
                'points': 3,
                'reason': 'Reason 1',
            },
            {
                'term_id': 2,
                'points': 4,
                'reason': 'Reason 2',
            },
            {
                'term_id': 3,
                'points': 9,
                'reason': ''
            },
            {
                'term_id': 5,
                'points': 2,
                'reason': '',
            }
        ]
    }

    res = client.post(url_termsignup, headers=[auth_header1], data=json.dumps(terms_signup_json),
                      content_type='application/json')

    assert res.status_code == 200
    assert res.json == {}

    terms_signups = list(TermSignup.query.all())
    assert len(terms_signups) == 4

    for sent_ts, db_ts in zip(terms_signup_json['terms_signup'], terms_signups):
        reason = sent_ts['reason']

        assert db_ts.user_id == 1
        assert db_ts.points == (sent_ts['points'] if not reason else 0)
        assert db_ts.reason == reason
        assert db_ts.reason_accepted is False
        assert db_ts.is_assigned is False
