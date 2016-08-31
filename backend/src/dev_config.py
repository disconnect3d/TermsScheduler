import os

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key')

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/dev.db'.format(os.path.dirname(os.path.realpath(__file__)))
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

CORS_ORIGINS = "*"

SETTINGS_IN_DB = (
    'MAX_PTS_PER_TERM', 'PTS_FOR_ALL', 'PTS_PER_SUB', 'PTS_PER_TERM',
    'SHOW_TERMS_RESULTS', 'SUBJECTS_SIGNUP', 'TERMS_SIGNUP'
)