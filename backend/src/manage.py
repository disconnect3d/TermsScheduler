#!/usr/bin/env python
import os

from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.script import Manager, Shell, Server

from application import create_app, db

# use dev config if env var is not set
config_file_path = os.environ.get('APP_CONFIG', None) or '../dev_config.py'

app = create_app(config_file_path)

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


def _make_context():
    """
    Return context dict for a shell session so one can access
    stuff without importing it explicitly.
    """
    return {'app': app, 'db': db}


manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()
