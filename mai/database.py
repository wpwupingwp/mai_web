#!/usr/bin/python3

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from mai import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    # email
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    register_date = db.Column(db.DateTime)
    address = db.Column(db.String(100))
    bider_id = db.relationship('Bid', backref='user')

    def __init__(self, username, password, address):
        self.username = username
        self.password = password
        self.register_date = datetime.utcnow()
        self.address = address

    def __repr__(self):
        return f'{self.username}'


class Goods(db.Model):
    __tablename__ = 'goods'
    goods_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # address for delivery
    address = db.Column(db.String(100))
    no_bid = db.Column(db.Boolean)
    description = db.Column(db.Text)
    highest_price = db.Column(db.Float)
    lowest_price = db.Column(db.Float)
    pub_date = db.Column(db.DateTime)
    expired_date = db.Column(db.DateTime)
    photo1 = db.Column(db.LargeBinary)
    photo2 = db.Column(db.LargeBinary)
    photo3 = db.Column(db.LargeBinary)
    # ?
    goods = db.relationship('Bid', backref='goods')


class Bid(db.Model):
    __tablename__ = 'bid'
    bid_id = db.Column(db.Integer, primary_key=True)
    bider_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.goods_id'))
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)


