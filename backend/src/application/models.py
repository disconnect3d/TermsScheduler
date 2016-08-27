from flask import g, current_app as app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import and_

from application import db, auth


class UserGroup(db.Model):
    __tablename__ = 'users_groups'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)


class SubjectGroup(db.Model):
    __tablename__ = 'subjects_groups'
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String, nullable=False)

    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def get_subjects(user_ids, additional_filter=None):
        f = UserGroup.user_id.in_(user_ids)

        if additional_filter:
            f = and_(additional_filter, f)

        return Subject.query.join(Subject.groups).filter(f).order_by(Subject.name)

    @staticmethod
    def has_subject(user_id, subject_id):
        return db.session.query(
            User.get_subjects([user_id], additional_filter=(Subject.id == subject_id)).exists()
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

    users = db.relationship("User", secondary="users_groups",
                            backref=db.backref('groups', lazy='dynamic'))

    subjects = db.relationship("Subject", secondary="subjects_groups",
                               backref=db.backref('groups', lazy='dynamic'))

    def __repr__(self):
        return "{id}: '{name}'".format(**self.__dict__)


class Subject(db.Model):
    __tablename__ = 'subjects'
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


class SubjectSignup(db.Model):
    __tablename__ = 'subjects_signup'
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)


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
