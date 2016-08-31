import pytest
from flask import url_for


@pytest.fixture(scope='session')
def url_settingslist():
    return url_for('settinglist')


def test_get_settings_unauthorized(url_settingslist, db, client):
    res = client.get(url_settingslist)
    assert res.status_code == 401


def test_get_settings_authorized(url_settingslist, auth_header1, db, client):
    res = client.get(url_settingslist, headers=[auth_header1])

    assert res.status_code == 200
    assert res.json == {'settings': []}
