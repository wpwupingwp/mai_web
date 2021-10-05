#!/usr/bin/python3

import flask as f
import flask_login as fl

from mai import lm
from mai.form import UserForm, GoodsForm, LoginForm
from mai.database import User, Goods, db

admin = f.Blueprint('admin', __name__)


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@admin.route('/login', methods=('POST', 'GET'))
def login():
    #if f.g.user is not None and f.g.user.is_authenticated():
    #    return f.redirect('/index')
    lf = LoginForm()
    if lf.validate_on_submit():
        user = User.query.filter_by(username=lf.username.data,
                                    password=lf.password.data).first()
        fl.login_user(user)
        f.flash(f'登陆成功 userid={user.user_id:06d}')
        print(user)
        return f.redirect('/index')
    return f.render_template('login.html', form=lf)


@admin.route('/logout', methods=('POST', 'GET'))
@fl.login_required
def logout():
    return f.redirect('/index')


@admin.route('/register', methods=('POST', 'GET'))
def register():
    print(f.request.path)
    uf = UserForm()
    if uf.validate_on_submit():
        user = User(uf.username.data, uf.password.data, uf.address.data)
        db.session.add(user)
        db.session.commit()
        f.flash('注册成功')
        return f.redirect('/index')
    else:
        print('bad form')
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