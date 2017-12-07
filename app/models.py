from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app



ROLE_USER = 0
ROLE_ADMIN = 1

# Order status
EXECUTED_ORDER = 0
NEW_ORDER = 1
IN_CART = 2


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), index = True, unique = True, nullable=False)
    password_hash = db.Column(db.String(64))
    role = db.Column(db.SmallInteger, nullable=False, default = ROLE_USER)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


    def __repr__(self):
        return '<User %r>' % (self.email)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_of_product = db.Column(db.String(512))
    size = db.Column(db.String(16))
    cost = db.Column(db.Float)
    product_description = db.Column(db.String(1024))
    img = db.Column(db.String(512))

    def __repr__(self):
        return '<Product %r>' % (self.name_of_product)


class User_account(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True, nullable=False)
    first_name = db.Column(db.String(124), nullable=False)
    last_name = db.Column(db.String(124), nullable=False)
    email = db.Column(db.String(64), unique = True, nullable=False)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


    def __repr__(self):
        return '%s' % self.full_name()


class Billing_address(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key = True)
    first_name = db.Column(db.String(124), nullable=False)
    last_name = db.Column(db.String(124), nullable=False)
    company_name = db.Column(db.String(124))
    email = db.Column(db.String(64), unique = True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String(124), nullable=False)
    apartment = db.Column(db.String(124), nullable=False)
    town = db.Column(db.String(124), nullable=False)
    state = db.Column(db.String(124), nullable=False)
    zip = db.Column(db.Integer, nullable=False)


class Shipping_address(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key = True)
    first_name = db.Column(db.String(124), nullable=False)
    last_name = db.Column(db.String(124), nullable=False)
    company_name = db.Column(db.String(124))
    email = db.Column(db.String(64), unique = True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String(124), nullable=False)
    apartment = db.Column(db.String(124), nullable=False)
    town = db.Column(db.String(124), nullable=False)
    state = db.Column(db.String(124), nullable=False)
    zip = db.Column(db.Integer, nullable=False)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_product = db.Column(db.Integer,  nullable=False)
    id_user = db.Column(db.Integer, nullable=False)
    order_status = db.Column(db.SmallInteger, nullable = False, default = IN_CART)









