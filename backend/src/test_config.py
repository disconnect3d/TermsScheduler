import os

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key')

SQLALCHEMY_DATABASE_URI = 'sqlite://'  # SQLite :memory: database
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

DEBUG = True
