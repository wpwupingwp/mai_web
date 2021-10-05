#!/usr/bin/python3

import flask as f
import flask_login as fl

from mai import lm
from mai.form import UserForm, GoodsForm, LoginForm
from mai.database import User, Goods, db

admin = f.Blueprint('admin', __name__)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@admin.route('/login', methods=('POST', 'GET'))
def login():
    lf = LoginForm()
    if lf.validate_on_submit():
        fl.login_user(user)
        f.flash('登陆成功')
        return f.redirect('/index')
    return f.render_template('login.html', form=lf)


@admin.route('/logout', methods=('POST', 'GET'))
@fl.login_required
def logout():
    return f.redirect('/index')


@admin.route('/register', methods=('POST', 'GET'))
def register():
    uf = UserForm()
    if uf.validate_on_submit():
        user = User(uf.username.data, uf.password.data, uf.address.data)
        db.session.add(user)
        db.session.commit()
        f.flash('Register OK')
        print('ok')
        return f.redirect('user')
    return f.render_template('register.html', form=uf)


@admin.route('/add_goods', methods=('POST', 'GET'))
@fl.login_required
def add_goods():
    gf = GoodsForm()
    if gf.validate_on_submit():
        goods = Goods(gf)
        db.session.add(goods)
        db.session.commit()
        f.flash('添加物品成功')
        print('ok')
        return f.redirect('goods')
    else:
        print(gf.errors)
    return f.render_template('add_goods.html', form=gf)