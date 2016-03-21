import os

basedir = os.path.abspath(os.path.dirname(__file__))
f = open(os.path.join(basedir, 'app.vars') , 'r')

CSRF_ENABLED = True

# uncomment out these next 4 lines if using mysql, comment out sqlite line
"""
MYSQL_DB = f.readline().strip()
MYSQL_HOST = f.readline().strip()
MYSQL_USERNAME = f.readline().strip()
MYSQL_PASSWORD = f.readline().strip()
SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USERNAME + ":" + MYSQL_PASSWORD + "@" + MYSQL_HOST + ":3306/" + MYSQL_DB
"""
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECURITY_TRACKABLE = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
SECRET_KEY = f.readline().strip()
SECURITY_PASSWORD_HASH = f.readline().strip()
SECURITY_PASSWORD_SALT = f.readline().strip()
FIRST_USER_NAME = f.readline().strip()
FIRST_USER_PASS = f.readline().strip()
f.close()
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')
