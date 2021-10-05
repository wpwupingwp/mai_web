#!/usr/bin/python3

import flask as f

# import flask_mail

from mai import app, lm
from mai.database import User, Goods, Bid, db
from mai.admin import admin


@app.route('/')
@app.route('/index')
def index():
    return f.render_template('index.html')


@app.route('/goods')
def goods():
    # ? add paginate
    return f.render_template('goods.html', goods=Goods.query.all())


@app.route('/user')
def user():
    # bootstrap requires same function name?
    print(User.query.all())
    return f.render_template('user.html', users=User.query.all())


@app.route('/user/<username>')
def manage_user(username):
    # /templates/user.html
    return f.render_template(
        'user.html', users=User.query.filter_by(username=username).all())


app.register_blueprint(admin, url_prefix='/admin')
