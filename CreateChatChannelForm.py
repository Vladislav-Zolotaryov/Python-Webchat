from flask.ext.wtf import Form

from wtforms import TextField, TextAreaField
from wtforms.validators import Required, DataRequired

class CreateChatChannelForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')