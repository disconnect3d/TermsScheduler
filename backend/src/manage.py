#!/usr/bin/env python
import inspect
import os

from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.script import Manager, Shell
from termcolor import colored, cprint

from application import create_app, db
# use dev config if env var is not set
from commands.add_dev_data import AddDevData
from commands.create_admin import CreateAdmin

config_file_path = os.environ.get('APP_CONFIG', None) or '../dev_config.py'

app = create_app(config_file_path)

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('create_admin', CreateAdmin())
manager.add_command('add_dev_data', AddDevData())


def logsql():
    """
    Enables/disables logging of SQLALchemy sql queries.
    """
    import logging
    logging.basicConfig()
    logger = logging.getLogger('sqlalchemy.engine')

    if logger.level == logging.NOTSET:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.NOTSET)


def _make_context():
    """
    Return context dict for a shell session so one can access
    stuff without importing it explicitly.
    """
    context_dict = {'app': app, 'db': db, 'logsql': logsql}

    def print_name(name, desc):
        name = colored(name, 'blue', attrs=['bold'])
        print('  {:15s} - {}'.format(name, desc))

    cprint('Names already imported to the shell (by `_make_context`):', 'yellow', attrs=['bold'])
    print_name('app', 'Flask application')
    print_name('db', 'flask.sqlalchemy database object')
    print_name('logsql', 'utility function to enable/disable logging of SQLAlchemy SQL queries')

    # Imports models from specified modules
    from application import models

    cprint('Models:', 'yellow', attrs=['bold'])
    for attr_name in dir(models):
        attr = getattr(models, attr_name)

        if inspect.isclass(attr) and issubclass(attr, db.Model):
            context_dict[attr.__name__] = attr
            print_name(
                attr.__name__,
                'imported from ' + colored(models.__name__ + '.' + attr.__name__, 'green')
            )

    return context_dict


manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    logsql()
    manager.run()
