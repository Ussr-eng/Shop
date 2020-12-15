from wtforms import Form, BooleanField, StringField, PasswordField,\
    validators, TextAreaField, SubmitField, ValidationError, IntegerField, SelectField, SelectMultipleField, RadioField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from .models import Register


class CustomerRegisterForm(FlaskForm):
    first_name = StringField('Имя: ',  [validators.Length(min=1, max=50), validators.DataRequired()])
    last_name = StringField('Фамилия: ',  [validators.Length(min=1, max=50), validators.DataRequired()])
    mobile = IntegerField('Номер телефона: ', validators=[validators.required()])
    email = EmailField('Электронная почта:', [validators.Length(min=4, max=20), validators.DataRequired()])
    password = PasswordField('Пароль: ', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Пароли не соответствуют')])
    confirm = PasswordField('Повторите пароль: ', [validators.DataRequired()])



    # !!!!!!!!!!поверяет поле number на уникальность!!!!!!!!!!
    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("Этот email уже используеться")


class UserOrderForm(FlaskForm):
    first_name = StringField('Имя: ', [validators.Length(min=1, max=50), validators.DataRequired()])
    last_name = StringField('Фамилия: ', [validators.Length(min=1, max=50), validators.DataRequired()])
    mobile = IntegerField('Номер телефона: ', validators=[validators.required()])
    callback = SelectField('Перезвонить ли вам?', [DataRequired()],
                          choices=[('Перезвонить', 'Перезвонить перед отправкой заказа'),
                                   ('Без звонка', 'Отправить заказ без звонка')]
                          )
    description = TextAreaField('Комментарий: ', [validators.Length(min=0, max=200)])


class CustomerLoginForm(FlaskForm):
    email = EmailField('Электронная почта:', [validators.Length(min=4, max=20), validators.DataRequired()])
    password = StringField('Пароль: ', [validators.DataRequired()])
    # submit = SubmitField('Login')
