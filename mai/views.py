#!/usr/bin/python3

import flask as f

# import flask_mail

from mai import app, lm, root
from mai.database import User, Goods, Bid
from mai.auth import auth


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
    pagination = Goods.query.paginate(page=page, per_page=per_page)
    return f.render_template('goods_list.html', pagination=pagination)


@app.route('/goods/<int:goods_id>')
def view_goods(goods_id):
    goods = Goods.query.get(goods_id)
    bids = Bid.query.filter_by(goods_id=goods_id
                               ).order_by(Bid.price.desc()).limit(5)
    return f.render_template('goods.html', goods=goods, bids=bids)


app.register_blueprint(auth, url_prefix='/auth')
