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
    # status
    failed_login = db.Column(db.Integer, default=0)
    failed_bid = db.Column(db.Integer, default=0)

    goods = db.relationship('Goods', backref='user')

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
    description = db.Column(db.Text, nullable=False)
    # price
    original_price = db.Column(db.Float)
    highest_price = db.Column(db.Float, nullable=False)
    lowest_price = db.Column(db.Float, nullable=False)
    # date
    pub_date = db.Column(db.DateTime)
    expired_date = db.Column(db.Date)
    # photo
    photo1 = db.Column(db.String(100))
    photo2 = db.Column(db.String(100))
    photo3 = db.Column(db.String(100))
    # others
    deleted = db.Column(db.Boolean, default=False)
    sold = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                        nullable=False)
    bids = db.relationship('Bid', backref='goods')

    def __repr__(self):
        return f'{self.goods_id},{self.name}'

    @staticmethod
    def from_form(form, user_id):
        goods_ = Goods()
        if isinstance(form, FlaskForm):
            goods_.name = form.name.data
            goods_.description = ''.join(form.description.data)
            goods_.address = form.address.data
            goods_.original_price = form.original_price.data
            goods_.highest_price = form.highest_price.data
            goods_.lowest_price = form.lowest_price.data
            goods_.expired_date = form.expired_date.data
            goods_.pub_date = datetime.now()
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
    is_buying = db.Column(db.Boolean, default=False)
    is_failed = db.Column(db.Boolean, default=False)

    def __init__(self, bider_id, goods_id, price):
        self.bider_id = bider_id
        self.goods_id = goods_id
        self.price = price
        self.date = datetime.utcnow()


class Message(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    to_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    bid_id = db.Column(db.Integer, db.ForeignKey('bid.bid_id'))
    date = db.Column(db.DateTime)
    content = db.Column(db.String(100))
    is_accept = db.Column(db.Boolean, default=False)
    is_read = db.Column(db.Boolean, default=False)
    is_report = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    from_ = db.relationship('User', backref='send', foreign_keys=[from_id])
    to_ = db.relationship('User', backref='receive', foreign_keys=[to_id])
    # bid_msg = db.relationship('Message', backref='bid_msg', foreign_keys=[bid_id])

    def __init__(self, from_id, to_id, bid_id, content):
        self.from_id = from_id
        self.to_id = to_id
        self.bid_id = bid_id
        self.content = content
        self.date = datetime.now()


class Visit(db.Model):
    __tablename = 'visitor'
    visit_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    ip = db.Column(db.String(100))
    url = db.Column(db.String(100))
    useragent = db.Column(db.String(200))
    date = db.Column(db.DateTime)
    user = db.relationship('User', backref='visit')

    def __init__(self, user_id, ip, url, useragent):
        self.user_id = user_id
        self.ip = ip
        self.url = url
        self.useragent = useragent
        self.date = datetime.now()

    def __str__(self):
        return (f'{self.date}:\t{self.user}\t{self.ip}'
                f'\t{self.url}\t{self.useragent}')


class MyModelView(ModelView):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def is_accessible(self):
        return (fl.current_user.is_authenticated and
                fl.current_user.username=='admin')

    def is_accessible_callback(self):
        return redirect('/')


for m in [User, Goods, Bid, Message, Visit]:
    admin.add_view(MyModelView(m, db.session))
