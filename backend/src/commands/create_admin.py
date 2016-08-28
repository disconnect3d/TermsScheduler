from flask.ext.script import Command, prompt
from flask.ext.script.cli import prompt_pass

from application import db
from application.models import User


class CreateAdmin(Command):
    """Creates admin account."""

    def run(self):
        username = prompt('Input username')
        password = prompt_pass('Input password')

        email = ''
        while '@' not in email:
            email = prompt('Email (requires "@")')

        first_name = prompt('First name (default: "")', default='')
        last_name = prompt('Last name (default: "")', default='')

        u = User(username=username, first_name=first_name, last_name=last_name, email=email, is_admin=True)
        u.hash_password(password)

        db.session.add(u)
        db.session.commit()

        print("User {} successfully added.".format(username))
