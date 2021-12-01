#!/usr/bin/python3

import flask as f
from flask import g
import flask_login as fl
from sqlalchemy import not_, and_

# import flask_mail

from mai import app, lm, root
from mai.database import User, Goods, Message, Bid, db
from mai.auth import auth
from mai.form import BidForm


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f.send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@lm.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user


@app.route('/favicon.ico')
def favicon():
    return f.send_from_directory(root/'static', 'favicon.png',
                                 mimetype='image/png')


@app.before_request
def get_unread():
    g.unread = Message.query.filter(and_(
        Message.to_id==fl.current_user.user_id, not_(Message.is_read),
        not_(Message.is_deleted))).count()
    print(g.unread)

@app.route('/')
@app.route('/index')
def index():
    return f.render_template('index.html')


@app.route('/readme')
def readme():
    return f.render_template('readme.html')


@app.route('/goods_list')
@app.route('/goods_list/<int:page>')
def goods_list(page=1):
    per_page = 6
    pagination = Goods.query.filter_by(deleted=False, sold=False).paginate(
        page=page, per_page=per_page)
    return f.render_template('goods_list.html', pagination=pagination)


@app.route('/goods/<int:goods_id>', methods=('POST', 'GET'))
def view_goods(goods_id):
    goods = Goods.query.get(goods_id)
    bids = db.session.query(Bid, User).join(
        Bid, Bid.bider_id==User.user_id).filter_by(
        goods_id=goods_id).order_by(Bid.price.desc()).limit(10)
    bidform = BidForm()
    if bidform.validate_on_submit():
        if not goods.lowest_price <= bidform.price.data <= goods.highest_price:
            f.flash('无效价格，请注意价格范围', category='error')
            return f.redirect(f.request.url)
        bid = Bid(fl.current_user.user_id, goods_id, bidform.price.data)
        db.session.add(bid)
        db.session.commit()
        f.flash('出价成功')
    return f.render_template('goods.html', goods=goods, bids=bids,
                             inline_form=bidform)


app.register_blueprint(auth, url_prefix='/auth')
