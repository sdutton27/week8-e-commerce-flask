from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
# import requests
from werkzeug.security import generate_password_hash

from secrets import token_hex # this returns a random hex string in hexadecimal

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable = False)
    last_name = db.Column(db.String(45), nullable = False)
    username = db.Column(db.String(45), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    is_admin = db.Column(db.Boolean, default=False)

    # new for API
    apitoken = db.Column(db.String, nullable = False, unique=True)

    # in_cart = db.relationship("Product", secondary = "cart")
    
    # I think we want something more like this
    # products = db.relationship('Product', secondary = "cart", back_populates='cart_owner', lazy=True, uselist=False)

    products = db.relationship('Product', secondary = 'cart', backref='cart_owner', lazy=True)

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def add_to_cart(self, product):
        self.products.append(product) 
        db.session.commit()

    def remove_from_cart(self, product):
        self.products.remove(product) 
        db.session.commit()

    def empty_cart(self):
        self.products.clear() 
        db.session.commit()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_changes(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # added this for JSON
    def to_dict(self):
        return {
            'id' : self.id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'username' : self.username,
            'email' : self.email, 
            'date_created' : self.date_created,
            'is_admin' : self.is_admin,
            # not sure if we want to put products in here
            # we cannot put this here because it does not update with the user json every time a product is added.
            #'products' : [prod.to_dict() for prod in self.products],
            'apitoken' : self.apitoken # we have to have this in here
        }

class Product(db.Model, UserMixin):
    # id, title, price, image, department=categories[0], link (to amazon), description, rating
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(300), unique = True, nullable = False)
    price = db.Column(db.Float, nullable = False)
    image = db.Column(db.String, nullable = False, unique = True)
    department = db.Column(db.String(30), nullable = False)
    amazon_link = db.Column(db.String, nullable = False)

    # From Simon- had I realized the descriptions were surrounded by "," then I 
    # would make this a list and split the description at "," and print the 
    # bulleted list out as a ul with li objects for each item in the list. 
    # However our free trial has run out so we can't add any objects.
    description = db.Column(db.String, nullable = False) 
    rating = db.Column(db.Float, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    in_cart = db.relationship("User", secondary = "cart", overlaps="cart_owner,products")
    #cart_owner = db.relationship('User', secondary="cart", back_populates='products_in_cart', lazy=True)

    def __init__(self, title, price, image, department, amazon_link, description, rating):
        self.title = title
        self.price = price
        self.image = image
        self.department = department
        self.amazon_link = amazon_link
        self.description = description
        self.rating = rating

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_changes(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # added this for JSON
    def to_dict(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'price' : self.price,
            'image' : self.image,
            'department' : self.department,
            'amazon_link' : self.amazon_link,
            'description' : self.description,
            'rating' : self.rating,
            'date_created' : self.date_created,
            # not sure if we want to put in_cart here
        }

cart = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)


class Checkout(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(300), nullable = False, unique = True)
    card_number = db.Column(db.String(10), nullable = False)
    expiration_date = db.Column(db.Integer, nullable = False)
    cvv = db.Column(db.String(3), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

    
    def __init__(self, name, email, address, card_number, expiration_date, cvv):
        self.name = name
        self.email = email
        self.address = address
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_changes(self):
        db.session.commit()