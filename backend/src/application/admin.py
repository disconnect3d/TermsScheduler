from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField

from application.models import User, Term, TermSignup, Setting


class UserAdminView(ModelView):
    form_columns = ('username', 'password', 'email', 'first_name', 'last_name', 'is_admin', 'groups')
    column_list = ('id', 'username', 'email', 'first_name', 'last_name', 'is_admin', 'groups')

    column_exclude_list = ('password_hash',)
    form_excluded_columns = ('password_hash',)

    form_extra_fields = {
        'password': PasswordField('Password')
    }

    form_base_class = SecureForm  # generates anti-CSRF tokens

    def on_model_change(self, form, model, is_created):
        changed_pwd = form.password.data

        if changed_pwd:
            model.hash_password(changed_pwd)


class SubjectAdminView(ModelView):
    column_list = (
        'id', 'name', 'description', 'syllabus_url', 'ects', 'minimum_members', 'maximum_members',
        'lecture_hours', 'lab_hours', 'exercises_hours', 'project_hours', 'seminar_hours',
        'groups'
    )


class TermAdminView(ModelView):
    column_list = (
        'id', 'type', 'day', 'time_from', 'time_to', 'groups'
    )


class TermSignupAdminView(ModelView):
    column_list = (
        User.first_name, User.last_name,
        Term.subject_id, Term.day, Term.time_from,
        TermSignup.points,
        TermSignup.reason, TermSignup.reason_accepted, TermSignup.reason_accepted_by,
        TermSignup.is_assigned
    )


class SettingAdminView(ModelView):
    column_display_pk = True
