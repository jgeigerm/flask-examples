from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Length
from flask import flash

class FormFlash(Form):
    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash("{} - {}".format(field, error), category="error")

class ExampleForm(FormFlash):
    user = SelectField('User', choices=[])
    anumber = IntegerField('A number', validators=[DataRequired()], default="")
    text = TextField('Enter some text!', default="this is the default", validators=[Length(min=3, max=50)])
    checkbox = BooleanField('Checkbox!')
    submit = SubmitField('submit')

    def validate_anumber(self, field):
        if field.data < 0:
            raise ValidationError("Try positive numbers ONLY!")
