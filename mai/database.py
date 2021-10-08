#!/usr/bin/python3

from datetime import datetime
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
import flask_login as fl

from mai import app, admin
from flask_wtf import FlaskForm

db = SQLAlchemy(app)


class User(db.Model, fl.UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    # email
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    register_date = db.Column(db.DateTime)
    address = db.Column(db.String(100))
    bider_id = db.relationship('Bid', backref='user')

    def __init__(self, username, password, address=''):
        self.username = username
        self.password = password
        self.register_date = datetime.utcnow()
        self.address = address

    def __repr__(self):
        return f'{self.username}'

    def get_id(self):
        return str(self.user_id)


class Goods(db.Model):
    __tablename__ = 'goods'
    goods_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # address for delivery
    address = db.Column(db.String(100))
    no_bid = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, nullable=False)
    original_price = db.Column(db.Float)
    highest_price = db.Column(db.Float, nullable=False)
    lowest_price = db.Column(db.Float, nullable=False)
    pub_date = db.Column(db.DateTime)
    expired_date = db.Column(db.Date)
    photo1 = db.Column(db.String(100))
    photo2 = db.Column(db.String(100))
    photo3 = db.Column(db.String(100))
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.goods_id},{self.name}'

    @staticmethod
    def from_form(form, user_id):
        goods_ = Goods()
        if isinstance(form, FlaskForm):
            goods_.name = form.name.data
            goods_.description = ''.join(form.description.data)
            goods_.address = form.address.data
            goods_.no_bid = form.no_bid.data
            goods_.original_price = form.original_price.data
            goods_.highest_price = form.highest_price.data
            goods_.lowest_price = form.lowest_price.data
            goods_.expired_date = form.expired_date.data
            goods_.pub_data = datetime.utcnow()
            goods_.user_id = user_id
        else:
            pass
        return goods_


class Bid(db.Model):
    __tablename__ = 'bid'
    bid_id = db.Column(db.Integer, primary_key=True)
    bider_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.goods_id'))
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)

    def __init__(self, bider_id, goods_id, price):
        self.bider_id = bider_id
        self.goods_id = goods_id
        self.price = price
        self.date = datetime.utcnow()


class MyModelView(ModelView):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def is_accessible(self):
        return (fl.current_user.is_authenticated and
                fl.current_user.username=='admin@example.com')

    def is_accessible_callback(self):
        return redirect('/')


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Goods, db.session))
admin.add_view((MyModelView(Bid, db.session)))
