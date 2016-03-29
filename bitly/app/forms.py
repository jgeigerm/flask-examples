from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length
from flask import flash
from app.models import Link
import string
import re

"""
FlashForm: Adds a flash_errors function that will flash errors on the screen
Parent: flask.ext.wft.Form
"""
class FormFlash(Form):

    """flash_errors: iterate through form errors and flash them to the screen"""
    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash("{} - {}".format(field, error), category="error")


"""
ExampleForm: an example form showing different input types and validators
Parent: .FlashForm
"""
class LinkForm(FormFlash):
    choices = [ (x,x) for x in ["minutes", "hours", "days", "weeks", "months"] ]
    link = TextField("Link to shorten: ", validators=[DataRequired(), Length(max=5000)])
    suffix = TextField("URL on this site (leave blank for random): ")
    expnum = TextField("Expire in (leave blank for never): ")
    exptype = SelectField("type", choices=choices)
    submit = SubmitField('submit')

    def validate_link(self, field):
        r = re.compile('https?://.*')
        if not r.match(field.data):
            raise ValidationError("That doesn't look like a valid URL...")

    def validate_expnum(self, field):
        if field.data == "":
            return
        if int(field.data) < 1:
            raise ValidationError("Number must be greater than 0")

    def validate_suffix(self, field):
        acceptablechars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        if [x for x in field.data if x not in acceptablechars]:
            raise ValidationError("Only alphanumeric characters are allowed")
        query = Link.query.filter_by(suffix=field.data).first()
        if (query and not query.is_expired):
            raise ValidationError("A link with that suffix exists and has not expired (valid until {})".format(query.get_expiry))
