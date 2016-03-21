from flask.ext.admin import AdminIndexView, BaseView
from flask.ext.admin.contrib.sqla.view import ModelView
from flask.ext.security import current_user, utils
from wtforms import PasswordField, validators
from flask import redirect, url_for, flash

class AdminBaseView(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('admin'):
            return True
        return False

    def _handle_view(self, name, **kwargs):
            if not self.is_accessible():
                flash("You don't have permission to go there", category="warning")
                return redirect(url_for('main.index'))

class AdminIndexView(AdminIndexView, AdminBaseView):
    pass

class AdminModelView(ModelView, AdminBaseView):
    pass

class UserModelView(AdminModelView):
    column_exclude_list = ['password']
    form_excluded_columns = ['last_login_at', 'current_login_at',
                             'last_login_ip', 'current_login_ip',
                             'login_count']
    form_overrides = dict(password=PasswordField)
    form_extra_fields = {'password2': PasswordField('Confirm Password',
                                                    [validators.EqualTo('password', message='Passwords must match')])}
    form_columns = ('roles', 'email', 'password', 'password2', 'active')

    #make sure the password is actually encrypted when it is changed or created!
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = utils.encrypt_password(model.password)


class RoleModelView(AdminModelView):
    pass
