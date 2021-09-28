#!/usr/bin/python3

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from mai import app
from mai.form import GoodsForm

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
    name = db.Column(db.String(100), nullable=False)
    # address for delivery
    address = db.Column(db.String(100))
    no_bid = db.Column(db.Boolean)
    description = db.Column(db.Text, nullable=False)
    original_price = db.Column(db.Float)
    highest_price = db.Column(db.Float, nullable=False)
    lowest_price = db.Column(db.Float, nullable=False)
    pub_date = db.Column(db.DateTime)
    expired_date = db.Column(db.DateTime)
    photo1 = db.Column(db.LargeBinary)
    photo2 = db.Column(db.LargeBinary)
    photo3 = db.Column(db.LargeBinary)

    def __init__(self, form):
        if isinstance(form, GoodsForm):
            self.name = form.name.data
            self.description = form.description.data,
            self.address = form.address.data
            self.no_bid = form.no_bid.data
            self.original_price = form.original_price.data
            self.highest_price = form.highest_price.data
            self.lowest_price = form.lowest_price.data
            self.expired_date = form.expired_date.data
            self.pub_data = datetime.utcnow()
            if form.photo1.data is not None:
                self.photo1 = form.photo1.data
            if form.photo2.data is not None:
                self.photo2 = form.photo1.data
            if form.photo3.data is not None:
                self.photo3 = form.photo1.data

    pass


class Bid(db.Model):
    __tablename__ = 'bid'
    bid_id = db.Column(db.Integer, primary_key=True)
    bider_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.goods_id'))
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)


