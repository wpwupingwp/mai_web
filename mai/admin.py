#!/usr/bin/python3

import flask as f
import flask_login as fl
from werkzeug.utils import secure_filename

from mai import lm, root
from mai.form import UserForm, GoodsForm, LoginForm
from mai.database import User, Goods, db

admin = f.Blueprint('admin', __name__)
# cannot use photos.url
img_path = root / 'upload' / 'img'


@lm.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user


@admin.route('/login', methods=('POST', 'GET'))
def login():
    #if f.g.user is not None and f.g.user.is_authenticated():
    #    return f.redirect('/index')
    lf = LoginForm()
    if lf.validate_on_submit():
        user = User.query.filter_by(username=lf.username.data,
                                    password=lf.password.data).first()
        if user is None:
            f.flash('用户不存在')
        else:
            fl.login_user(user)
            f.flash(f'登陆成功')
            return f.redirect('/index')
    return f.render_template('login.html', form=lf)


@admin.route('/logout', methods=('POST', 'GET'))
@fl.login_required
def logout():
    fl.logout_user()
    return f.redirect('/index')


@admin.route('/register', methods=('POST', 'GET'))
def register():
    uf = UserForm()
    if uf.validate_on_submit():
        username = User.query.filter_by(username=uf.username.data).first()
        if username is not None:
            f.flash('用户名已注册')
            return f.render_template('register.html', form=uf)
        user = User(uf.username.data, uf.password.data, uf.address.data)
        db.session.add(user)
        db.session.commit()
        f.flash('注册成功')
        return f.redirect('/index')
    return f.render_template('register.html', form=uf)


def upload(data, path) -> str:
    """
    Return '' if not exists.
    Args:
        data: request.file.data
        path: str
    Returns: str
    """
    if data is None:
        return ''
    # relative path
    filename = secure_filename(data.filename)
    # absolute path
    data.save(path/filename)
    # relative path
    url = f.url_for('uploaded_file', filename=filename)
    return url


@admin.route('/add_goods', methods=('POST', 'GET'))
@fl.login_required
def add_goods():
    gf = GoodsForm()
    if gf.validate_on_submit():
        goods = Goods(gf, fl.current_user.user_id)
        goods.photo1 = upload(gf.photo1.data, img_path)
        goods.photo2 = upload(gf.photo2.data, img_path)
        goods.photo3 = upload(gf.photo3.data, img_path)
        db.session.add(goods)
        db.session.commit()
        f.flash('添加物品成功')
        print('ok')
        return f.redirect('/goods')
    return f.render_template('add_goods.html', form=gf)