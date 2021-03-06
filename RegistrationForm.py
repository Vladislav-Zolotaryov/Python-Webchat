from flask.ext.wtf import Form

from wtforms import TextField, PasswordField
from wtforms.validators import Required, DataRequired

class RegistrationForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirmation = PasswordField('Password confirmation', validators=[DataRequired()])