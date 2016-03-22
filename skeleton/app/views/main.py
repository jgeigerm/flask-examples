#!flask/bin/python
from app import db, app
from flask import render_template, g, Blueprint
from flask.ext.security import current_user, login_required
from app.models import *
from app.forms import *

# create a blueprint called main
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    return render_template("index.html")

@main.route('/examplepage')
@login_required
def examplepage():
    return render_template('examplepage.html', title="Example Page!")

@main.route('/exampleform', methods=['GET', 'POST'])
@login_required
def exampleform():
    form = ExampleForm()
    form.user.choices = [ (x.email, x.email) for x in User.query.all() ]
    if form.validate_on_submit():
        flash("Good job you filled out the form: {}, {}, {}, {}".format(form.user.data,
                                                                         form.anumber.data,
                                                                         form.text.data,
                                                                         form.checkbox.data),
              category="good")
    else:
        form.flash_errors()
    return render_template("exampleform.html", title="Example Form!", form=form)

