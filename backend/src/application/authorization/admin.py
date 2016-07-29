from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField


class UserAdminView(ModelView):
    form_columns = ('username', 'password', 'email', 'first_name', 'last_name', 'is_admin', 'groups')

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
