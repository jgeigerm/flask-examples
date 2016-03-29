#!flask/bin/python
from app import db
from flask import render_template, Blueprint, request, redirect, abort, session
from datetime import timedelta, datetime
from random import randint, choice
import string
from urlparse import urlparse
from app.models import *
from app.forms import *

# create a blueprint called main
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/create', methods=['GET', 'POST'])
def create():
    form = LinkForm()
    if form.validate_on_submit():
        suffix = form.suffix.data
        choices = string.ascii_uppercase + string.digits + string.ascii_lowercase
        while suffix == "":
            tmp = ''.join(choice(choices) for _ in range(randint(5, 10)))
            if not len(Link.query.filter_by(suffix=tmp).all()):
                suffix = tmp
        link = Link.query.filter_by(suffix=suffix).first()
        try:
            tmptype = form.exptype.data
            tmpnum = int(form.expnum.data)
            if tmptype == "months":
                tmpnum *= 30
                tmptype = "days"
            timedict = {tmptype: int(tmpnum)}
            td = timedelta(**timedict)
        except: td = timedelta()
        expiry = datetime.now() + td
        if form.expnum.data == "":
            expiry = None
        if link:
            link.expiry = expiry
            link.link = form.link.data
        else:
            link = Link(suffix=suffix, link=form.link.data, expiry=expiry)
        db.session.add(link)
        db.session.commit()
        session['links'].append({"link": link.link, "expiry": link.get_expiry, "suffix": link.suffix})
        u = urlparse(request.base_url)
        flash('Your link is {}://{}/{}'.format(u.scheme, u.netloc, suffix), category='good')
    else:
        form.flash_errors()
    return render_template("exampleform.html", title="Create link", form=form, links=session['links'])

@main.route('/<suffix>')
def link(suffix):
    try:
        link = Link.query.filter_by(suffix=suffix).one()
    except: abort(404)
    if not link.is_expired:
        return redirect(link.link)
    abort(404)
