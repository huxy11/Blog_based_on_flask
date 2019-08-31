from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, EqualTo, Length

class NameForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[Required()])
    submit = SubmitField('Submit.')

class LogInForm(FlaskForm):
    username = StringField('Account', validators=[Required()])
    sumbit = SubmitField('Log in.')

class CommentForm(FlaskForm):
    body = TextAreaField('Leave a message.', validators=[Required()])
    sumbmit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = TextAreaField('Tile', validator=[Required(), Length(1, 32)])
    body = PageDownField('Content', validator=[Required()])
    submit = SubmitField('Submit')
