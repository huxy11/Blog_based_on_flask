from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Required, Regexp, Length, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    account = StringField('Account', validators=[Required()])
    password = PasswordField('Password.', validators=[Required()])
    remember_me = BooleanField('Keep me logged in.')
    submit = SubmitField('Login.')

class RegistrationForm(Form):
    account = StringField('Account.', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores.')])
    password = PasswordField('Password.', validators=[Required(), EqualTo('password_cfm', message = 'Passwords must match.')])
    password_cfm = PasswordField('Confirm password.', validators=[Required()])
    submit = SubmitField('Register')

    def validate_account(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password.', validators=[Required()])
    password = PasswordField('Password.', validators=[Required(), EqualTo('password_cfm', message = 'Passwords must match.')])
    password_cfm = PasswordField('Confirm password.', validators=[Required()])
    submit = SubmitField('ChangePassword')


class EditProfileForm(Form):
    location = StringField('Location.', validators=[Length(0, 64)])
    about_me = StringField('About me.', validators=[Length(0,128)])
    submit = SubmitField('Submit')

class AdminIdQueryForm(Form):
    id = StringField('ID.', validators=[Required(), Regexp('[0-9]+', 0, 'ID must have only numbers.')])
    submit = SubmitField('Query')

class UserProfileForm(Form):
    account = StringField('Account.', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores.')])
    location = StringField('Location.', validators=[Length(0,64)])
    about_me = StringField('About me.', validators=[Length(0,64)])
    submit = SubmitField('Submit')
