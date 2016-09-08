import datetime
import random
from itertools import count

from flask.ext.script import Command
from passlib.apps import custom_app_context as pwd_context

from application import db
from application.enums import TermType, Day
from application.models import User, Group, UserGroup, Subject, SubjectGroup, Term, Setting, TermGroup


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

        subjects = [
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
        db.session.execute(Subject.__table__.insert(), subjects)

        db.session.execute(
            SubjectGroup.__table__.insert(),
            [
                {'subject_id': i, 'group_id': 1} if i < 6 else {'subject_id': i, 'group_id': 2} for i in range(1, 10)
                ]
        )

        random.seed(1)
        seq = count()

        def term_stub(subject):
            days = list(Day.__members__.keys())
            hour = random.randrange(8, 18)
            return {
                'id': next(seq),
                'subject_id': subject['id'],
                'type': TermType.lab,
                'day': random.choice(days),
                'time_from': datetime.time(hour),
                'time_to': datetime.time(hour + 1)
            }

        terms = [term_stub(s) for x in range(0, 3) for s in subjects]
        db.session.execute(Term.__table__.insert(), terms)

        db.session.execute(TermGroup.__table__.insert(), [{'term_id': t['id'], 'group_id': 1} for t in terms])

        db.session.execute(
            Setting.__table__.insert(),
            [
                {
                    'name': Setting.SUBJECTS_SIGNUP,
                    'value': '1'
                },
                {
                    'name': Setting.TERMS_SIGNUP,
                    'value': '1'
                },
                {
                    'name': Setting.SHOW_TERMS_RESULTS,
                    'value': '0'
                },

                # Terms signup related
                {
                    'name': Setting.PTS_FOR_ALL,  # Punkty dostępne dla wszystkich przedmiotów
                    'value': '14'
                },
                {
                    'name': Setting.PTS_PER_SUB,  # Punkty dostępne dla pojedynczego przedmiotu
                    'value': '15'
                },
                {
                    'name': Setting.PTS_PER_TERM,  # Punkty dostępne dla pojedynczego terminu
                    'value': '10'
                },
                {
                    'name': Setting.MAX_PTS_PER_TERM,
                    'value': '10'
                },
            ]
        )
