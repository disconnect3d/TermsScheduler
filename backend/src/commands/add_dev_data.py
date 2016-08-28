from flask.ext.script import Command
from passlib.apps import custom_app_context as pwd_context

from application import db
from application.models import User, Group, UserGroup, Subject, SubjectGroup


class AddDevData(Command):
    """Adds fake data, useful for development."""

    def run(self):
        pwd = pwd_context.encrypt('1234')

        db.session.execute(
            User.__table__.insert(),
            [
                {'id': 1, 'username': 'root', 'password_hash': pwd, 'email': 'a@a.a', 'first_name': 'John',
                 'last_name': 'Smith', 'is_admin': True},
                {'id': 2, 'username': 'user1', 'password_hash': pwd, 'email': 'a@a.a', 'first_name': 'John',
                 'last_name': 'Smith', 'is_admin': False},
                {'id': 3, 'username': 'user2', 'password_hash': pwd, 'email': 'a@a.a', 'first_name': 'Ed',
                 'last_name': 'Williams', 'is_admin': False},
                {'id': 4, 'username': 'user3', 'password_hash': pwd, 'email': 'a@a.a', 'first_name': 'Wendy',
                 'last_name': 'Jones', 'is_admin': False},
            ]
        )

        db.session.execute(
            Group.__table__.insert(),
            [
                {'id': 1, 'name': 'year 1'},
                {'id': 2, 'name': 'year 2'},
            ]
        )

        db.session.execute(
            UserGroup.__table__.insert(),
            [
                {'user_id': 1, 'group_id': 1},
                {'user_id': 1, 'group_id': 2},

                {'user_id': 2, 'group_id': 1},

                {'user_id': 3, 'group_id': 2},

                {'user_id': 4, 'group_id': 2},
            ]
        )

        def subject_stub(id, name):
            return {
                'id': id, 'name': name, 'description': '', 'syllabus_url': '', 'ects': 3,
                'minimum_members': 3, 'maximum_members': 10,
                'lecture_hours': 10, 'lab_hours': 10, 'exercises_hours': 10, 'project_hours': 10, 'seminar_hours': 10
            }

        db.session.execute(
            Subject.__table__.insert(),
            [
                subject_stub(1, 'Math 1'),
                subject_stub(2, 'Discrete math'),
                subject_stub(3, 'Unix'),
                subject_stub(4, 'Algebra'),
                subject_stub(5, 'Programming 1'),

                subject_stub(6, 'Math 2'),
                subject_stub(7, 'Programming 2'),
                subject_stub(8, 'Scripting languages'),
                subject_stub(9, 'Software engineering')
            ]
        )

        db.session.execute(
            SubjectGroup.__table__.insert(),
            [
                {'subject_id': i, 'group_id': 1} if i < 6 else {'subject_id': i, 'group_id': 2} for i in range(1, 10)
                ]
        )
