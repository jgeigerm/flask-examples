from app import app
from flask import render_template, g, session, request
from flask.ext.security import current_user
from urlparse import urlparse

"""
This file defines common application view handlers such as for 404's, 500's
and a function to run before every request is made.
"""

"""run before each request to any page on the app"""
@app.before_request
def before_request():
    # templates can get to the g object, so give them access to the user
    g.user = current_user
    u = urlparse(request.base_url)
    g.base_url = '{}://{}/'.format(u.scheme, u.netloc)
    if 'links' not in session.keys():
        session['links'] = list()

"""handle 404 errors (page not found error)"""
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title="fourohfour")

"""handle 500 errors (internal server error)"""
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', title="Internal server error :(")
