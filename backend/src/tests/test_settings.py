import pytest
from flask import url_for

from application.models import Setting
from test_config import SETTINGS_IN_DB


@pytest.fixture(scope='session')
def url_settingslist():
    return url_for('settinglist')


def test_get_settings_unauthorized(url_settingslist, db, client):
    res = client.get(url_settingslist)
    assert res.status_code == 401


def test_get_settings_authorized(url_settingslist, auth_header1, db, client):
    settings = [
        Setting(name=setting_name, value=setting_name+'_value')
        for setting_name in SETTINGS_IN_DB
    ]

    db.session.add_all(settings)
    db.session.commit()

    res = client.get(url_settingslist, headers=[auth_header1])

    assert res.status_code == 200
    assert res.json == {'settings': [
        {'name': v, 'value': v+'_value'} for v in SETTINGS_IN_DB
    ]}
