from flask import g, current_app as app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import and_, event
from sqlalchemy.orm import validates

from application import db, auth
from application.enums import Day, TermType


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String, nullable=False)

    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    signed_subjects = db.relationship('Subject', secondary='subjects_signup',
                                      backref=db.backref('signed_users', lazy='dynamic'))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def _get_for_groups(self, model, group_model, additional_filter=None):
        group_ids = [i.id for i in self.groups]

        f = group_model.group_id.in_(group_ids)
        if additional_filter:
            f = and_(f, additional_filter)

        return model.query.join(group_model).filter(f)

    def get_subjects(self):
        return self._get_for_groups(Subject, SubjectGroup).order_by(Subject.name)

    def has_subject(self, subject_id):
        return db.session.query(
            self._get_for_groups(Subject, SubjectGroup, additional_filter=(Subject.id == subject_id)).exists()
        ).scalar()

    def get_terms(self):
        return self._get_for_groups(Term, TermGroup)

    def has_term(self, term_id):
        return db.session.query(
            self._get_for_groups(Term, TermGroup, additional_filter=Term.id == term_id).exists()
        ).scalar()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        return User.query.get(data['id'])

    def __repr__(self):
        return "{id}: '{first_name}' '{last_name}', '{email}', admin: {is_admin}".format(**self.__dict__)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)

    users = db.relationship('User', secondary='users_groups',
                            backref=db.backref('groups', lazy='select'))

    subjects = db.relationship('Subject', secondary='subjects_groups',
                               backref=db.backref('groups', lazy='select'))

    terms = db.relationship('Term', secondary='terms_groups',
                            backref=db.backref('groups', lazy='select'))

    def __repr__(self):
        return self.name


class UserGroup(db.Model):
    __tablename__ = 'users_groups'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id), primary_key=True)


class Subject(db.Model):
    __tablename__ = 'subjects'

    def __json__(self):
        return (
            'id', 'name', 'description', 'syllabus_url', 'ects', 'minimum_members', 'maximum_members',
            'lecture_hours', 'lab_hours', 'exercises_hours', 'project_hours', 'seminar_hours'
        )

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(2048), nullable=False, default='')
    syllabus_url = db.Column(db.String(256), nullable=False, default='')

    # European Credit Transfer and Accumulation System points
    # see https://en.wikipedia.org/wiki/European_Credit_Transfer_and_Accumulation_System
    ects = db.Column(db.Integer, nullable=False, default=0)

    minimum_members = db.Column(db.Integer, nullable=False, default=5)
    maximum_members = db.Column(db.Integer, nullable=False, default=15)

    # hours
    lecture_hours = db.Column(db.Integer, nullable=False, default=0)
    lab_hours = db.Column(db.Integer, nullable=False, default=0)
    exercises_hours = db.Column(db.Integer, nullable=False, default=0)
    project_hours = db.Column(db.Integer, nullable=False, default=0)
    seminar_hours = db.Column(db.Integer, nullable=False, default=0)


class SubjectGroup(db.Model):
    __tablename__ = 'subjects_groups'
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id), primary_key=True)


class SubjectSignup(db.Model):
    __tablename__ = 'subjects_signup'
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)


class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id))
    type = db.Column(db.Enum(TermType), nullable=False)
    day = db.Column(db.Enum(Day), nullable=False)
    time_from = db.Column(db.Time, nullable=False)
    time_to = db.Column(db.Time, nullable=False)


class TermGroup(db.Model):
    __tablename__ = 'terms_groups'
    term_id = db.Column(db.Integer, db.ForeignKey(Term.id), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id), primary_key=True)


class TermSignup(db.Model):
    __tablename__ = 'terms_signup'
    term_id = db.Column(db.Integer, db.ForeignKey(Term.id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    points = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String, nullable=False, default='')

    reason_accepted = db.Column(db.Boolean, nullable=False, default=False)
    reason_accepted_by = db.Column(db.ForeignKey(User.id), nullable=True, default=None)

    is_assigned = db.Column(db.Boolean, nullable=False, default=False)


class Settings(db.Model):
    __tablename__ = 'settings'
    name = db.Column(db.String, primary_key=True)
    value = db.Column(db.String, primary_key=True)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
