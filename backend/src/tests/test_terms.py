from datetime import time
import pytest
from flask import json
from flask import url_for

from application.enums import TermType, Day
from application.models import Subject, SubjectSignup, Term


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
        Term(subject_id=1, type=TermType.lab, day=Day.monday, time_from=time(8, 30), time_to=time(10, 0), groups=[group1, group3]),
        Term(subject_id=1, type=TermType.lab, day=Day.tuesday, time_from=time(9, 30), time_to=time(11, 0), groups=[group1, group3]),
        Term(subject_id=1, type=TermType.lab, day=Day.wednesday, time_from=time(8, 30), time_to=time(10, 0), groups=[group1, group3]),

        Term(subject_id=2, type=TermType.lab, day=Day.friday, time_from=time(8, 30), time_to=time(10, 0)),

        Term(subject_id=3, type=TermType.lab, day=Day.tuesday, time_from=time(19, 0), time_to=time(21, 0)),
        Term(subject_id=3, type=TermType.lab, day=Day.thursday, time_from=time(11, 0), time_to=time(12, 30)),
    )

    for term in terms:
        db.session.add(term)
    db.session.commit()

    return terms


@pytest.fixture(scope='session')
def url_get_terms():
    # TODO / FIXME / WIP
    pass
    #return url_for('termslist')


def test_get_terms_for_user_unauthorized(url_get_terms, terms, db, client):
    res = client.get(url_get_terms)

    assert res.status_code == 401
