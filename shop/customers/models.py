from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json


@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)


class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=True)
    LastName =  db.Column(db.String(50), nullable=True)
    mobile = db.Column(db.String(15), unique=True, nullable=True)
    password = db.Column(db.String(202), unique= False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return '<Register %r>' % self.mobile





class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)



class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime(20), default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)


    def __repr__(self):
        return '<customerOrder %r>' % self.invoice



class CustomerOrderByOneClick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=False)
    number = db.Column(db.String(15), unique=False)
    product_name = db.Column(db.String(30), unique=False)
    product_price = db.Column(db.Numeric(10,2), nullable=False)
    product_discount = db.Column(db.String(30), unique=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)



db.create_all()