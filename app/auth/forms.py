from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import Required, Regexp, Length, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    account = StringField('Account', validators=[Required()])
    password = PasswordField('Password.', validators=[Required()])
    remember_me = BooleanField('Keep me logged in.')
    submit = SubmitField('Login.')

class RegistrationForm(FlaskForm):
    account = StringField('Account.', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores.')])
    password = PasswordField('Password.', validators=[Required(), EqualTo('password_cfm', message = 'Passwords must match.')])
    password_cfm = PasswordField('Confirm password.', validators=[Required()])
    submit = SubmitField('Register')

    def validate_account(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password.', validators=[Required()])
    password = PasswordField('Password.', validators=[Required(), EqualTo('password_cfm', message = 'Passwords must match.')])
    password_cfm = PasswordField('Confirm password.', validators=[Required()])
    submit = SubmitField('ChangePassword')


class EditProfileForm(FlaskForm):
    location = StringField('Location.', validators=[Length(0, 64)])
    about_me = StringField('About me.', validators=[Length(0,128)])
    submit = SubmitField('Submit')

class AdminIdQueryForm(FlaskForm):
    id = StringField('ID.', validators=[Required(), Regexp('[0-9]+', 0, 'ID must have only numbers.')])
    submit = SubmitField('Query')

class UserProfileForm(FlaskForm):
    username = StringField('Account.', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores.')])
    location = StringField('Location.', validators=[Length(0,64)])
    about_me = StringField('About me.', validators=[Length(0,64)])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[Required(), Length(1, 32)])
    body = PageDownField('Content', validators=[Required()])
    submit = SubmitField('Submit')
