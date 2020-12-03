from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, TextAreaField, DecimalField

class Addproducts(Form):
    name = StringField('name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0 )
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    # colors = TextAreaField('Colors', [validators.DataRequired()])

    image_1 = FileField('Image№1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('Image№2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Image№3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

    # image_2 = FileField('Image_2', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg']), 'images only images'])
    # image_3 = FileField('Image_3',validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg']), 'images only images'])

    # image_3 = FileField('Image 3', [FileRequired(), FileAllowed(['jpg, jpeg, png, svg, gif']), "Images Only please"])



