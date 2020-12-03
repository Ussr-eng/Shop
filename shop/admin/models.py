from shop import db

# registration
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    profile = db.Column(db.String(80), unique=False, nullable=False,
                        default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.username





#                 !!!!!!!!!!!!!-------сущности для новой почты-------!!!!!!!!!!!!!
#
# class NPCity(db.Model):
#     __tablename__ = 'np_cities'
#     id = db.Column(db.Integer, primary_key=True)
#     ref = db.Column(db.String(200), unique=True, nullable=False)
#     area = db.Column(db.String(150))
#     city = db.Column(db.String(150))
#     warehouses = db.relationship('NPWarehouse', backref='city')
#
#
# class NPWarehouse(db.Model):
#     __tablename__ = 'np_warehouses'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250))
#     number = db.Column(db.String(150))
#     ref = db.Column(db.String(150))
#     city_id = db.Column(db.Integer, db.ForeignKey('np_cities.id'))


class NPWarehouse(db.Model):
    __tablename__ = 'np_warehouses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))




db.create_all()