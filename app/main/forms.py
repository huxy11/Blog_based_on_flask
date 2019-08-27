from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, EqualTo

class NameForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[Required()])
    submit = SubmitField('Submit.')

class LogInForm(FlaskForm):
    username = StringField('Account', validators=[Required()])
    sumbit = SubmitField('Log in.')

