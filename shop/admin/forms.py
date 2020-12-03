from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, SelectField

class RegistrationForm(Form):
    name = StringField('name', [validators.Length(min=1, max=25)])
    username = StringField('Username', [validators.Length(min=1, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [validators.DataRequired()])


