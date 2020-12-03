from wtforms import Form, BooleanField, StringField, PasswordField,\
    validators, TextAreaField, SubmitField, ValidationError, IntegerField, SelectField, SelectMultipleField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register



class CustomerRegisterForm(FlaskForm):
    first_name =  StringField('Имя: ',  [validators.Length(min=1, max=50), validators.DataRequired()])
    last_name = StringField('Фамилия: ',  [validators.Length(min=1, max=50), validators.DataRequired()])
    mobile = StringField('Номер телефона: ',  [validators.Length(min=6, max=10), validators.DataRequired()])
    password = PasswordField('Пароль: ', [validators.DataRequired(), validators.EqualTo('confirm',
                                                                                         message='Passwords must match')])
    confirm = PasswordField('Повторите пароль: ', [validators.DataRequired()])

    submit = SubmitField('Регистрация')





    # !!!!!!!!!!поверяет поле number на уникальность!!!!!!!!!!
    def validate_number(self, mobile):
        if Register.query.filter_by(number=mobile.data).first():
            raise  ValidationError ("Этот номер уже используеться")



class CustomerLoginForm(FlaskForm):
    number = StringField('Номер: ', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = StringField('Пароль: ', [validators.DataRequired()])

    # submit = SubmitField('Login')



class OrderForm(FlaskForm):
    name = StringField('Имя: ', [validators.Length(min=3, max=20)])
    telephone = IntegerField('Номер телефона: ', [validators.NumberRange(min=0, max=12)])

    warehouse = StringField('Номер отделения: ', [validators.Length(min=3, max=100)])

