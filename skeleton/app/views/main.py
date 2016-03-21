#!flask/bin/python
from app import db, app
from flask import render_template, g, Blueprint
from app.models import *
from flask.ext.security import current_user, login_required

main = Blueprint('main', __name__)

@app.before_request
def before_request():
    g.user = current_user

@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    return render_template("index.html")

@main.route('/examplepage')
@login_required
def examplepage():
    return render_template('examplepage.html', title="Example Page!")

@main.errorhandler(404)
def not_found_error(error):
    return render_template('404.html')
