#!flask/bin/python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, utils
from config import FIRST_USER_PASS, FIRST_USER_NAME
from flask_wtf.csrf import CsrfProtect
from flask_admin.contrib.sqla import ModelView
from flask.ext.admin import Admin
from flask_admin.base import MenuLink

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
CsrfProtect(app)

from app import models
db.create_all()
db.session.commit()
userstore = SQLAlchemyUserDatastore(db, models.User, models.Role)
sec = Security(app, userstore)
try:
    with app.app_context():
        userstore.find_or_create_role(name='admin', description='Administrator')
        userstore.find_or_create_role(name='user', description='General user')
        userstore.create_user(email=FIRST_USER_NAME,
                            password=utils.encrypt_password(FIRST_USER_PASS))
        userstore.add_role_to_user('admin', 'admin')
        db.session.commit()
except: db.session.rollback()

from app.views import main, admin

app.register_blueprint(main.main)
app_admin = Admin(app, 'Flask Skeleton Admin', template_mode='bootstrap3', index_view=admin.AdminIndexView())
app_admin.add_view(admin.UserModelView(models.User, db.session))
app_admin.add_view(admin.RoleModelView(models.Role, db.session))
app_admin.add_link(MenuLink(name='Back to Site', url='/'))
