#!/usr/bin/python3

import flask as f
import flask_login as fl
from werkzeug.utils import secure_filename

from mai import app, lm, root
from mai.form import UserForm, GoodsForm, LoginForm
from mai.database import User, Goods, db

auth = f.Blueprint('auth', __name__)
# cannot use photos.url
img_path = root / 'upload' / 'img'


@lm.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user


@auth.route('/login', methods=('POST', 'GET'))
def login():
    #if f.g.user is not None and f.g.user.is_authenticated():
    #    return f.redirect('/index')
    lf = LoginForm()
    if lf.validate_on_submit():
        user = User.query.filter_by(username=lf.username.data).first()
        if user is None:
            f.flash('用户不存在')
        elif user.password != lf.password.data:
            user.failed_login += 1
            db.session.commit()
            try_n = app.config["MAX_LOGIN"] - user.failed_login
            if try_n > 0:
                f.flash(f'密码错误{user.failed_login}次，还可以尝试{try_n}次')
        elif user.failed_login >= app.config['MAX_LOGIN']:
            f.flash('登陆失败次数过多，账号已被锁定，如需解封请联系管理员。')
        elif user.failed_bid >= app.config['MAX_FAILED_BID']:
            f.flash('您的违约交易次数过多，账号已被锁定，如需解封请联系管理员。')
        else:
            fl.login_user(user)
            f.flash(f'登陆成功')
            return f.redirect('/index')
    return f.render_template('login.html', form=lf)


@auth.route('/logout', methods=('POST', 'GET'))
@fl.login_required
def logout():
    fl.logout_user()
    return f.redirect('/index')


@auth.route('/register', methods=('POST', 'GET'))
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
    if data is None or isinstance(data, str):
        return ''
    # relative path
    filename = secure_filename(data.filename)
    # absolute path
    data.save(path/filename)
    # relative path
    url = f.url_for('uploaded_file', filename=filename)
    return url


@auth.route('/add_goods', methods=('POST', 'GET'))
@fl.login_required
def add_goods():
    gf = GoodsForm()
    if gf.validate_on_submit():
        goods = Goods.from_form(gf, fl.current_user.user_id)
        goods.photo1 = upload(gf.photo1.data, img_path)
        goods.photo2 = upload(gf.photo2.data, img_path)
        goods.photo3 = upload(gf.photo3.data, img_path)
        db.session.add(goods)
        db.session.commit()
        f.flash('添加物品成功')
        return f.redirect(f'/auth/goods/{fl.current_user.user_id}')
    return f.render_template('add_goods.html', form=gf)


@auth.route('/delete_goods/<int:goods_id>')
@fl.login_required
def delete_goods(goods_id):
    goods = Goods.query.filter_by(goods_id=goods_id).first()
    if goods is None:
        f.flash('商品不存在')
    else:
        if goods.user_id != fl.current_user.user_id:
            f.flash('无权限删除')
        else:
            goods.deleted = True
            db.session.delete(goods)
            db.session.commit()
            f.flash('删除成功')
    return f.redirect(f'/auth/goods/{fl.current_user.user_id}')


@auth.route('/edit_goods/<int:goods_id>', methods=('POST', 'GET'))
@fl.login_required
def edit_goods(goods_id):
    goods = Goods.query.filter_by(goods_id=goods_id).first()
    gf = GoodsForm(obj=goods)
    print(gf.data, type(gf.data))
    if gf.validate_on_submit():
        new = dict(gf.data)
        new.pop('submit')
        new.pop('csrf_token')
        new['photo1'] = upload(gf.photo1.data, img_path)
        new['photo2'] = upload(gf.photo2.data, img_path)
        new['photo2'] = upload(gf.photo3.data, img_path)
        #new['expired_date'] = gf.expired_date.data
        #new['no_bid'] = True if new['no_bid']=='y' else False
        Goods.query.filter_by(goods_id=goods_id).update(new)
        db.session.commit()
        f.flash('修改物品成功')
        return f.redirect('/auth/goods/1')
    return f.render_template('add_goods.html', title='修改', form=gf)


@fl.login_required
@auth.route('/goods/<int:user_id>')
@auth.route('/goods/<int:user_id>/<int:page>')
def my_goods(user_id, page=1):
    per_page = 5
    if fl.current_user.is_anonymous:
        f.flash('请登录')
        return f.redirect('/auth/login')
    if user_id != fl.current_user.user_id:
        f.flash('仅可查看自己的商品')
        #return f.redirect(f.url_for('admin.login'))
        user_id = fl.current_user.user_id
    pagination = Goods.query.with_entities(
        Goods.goods_id, Goods.name, Goods.pub_date, Goods.original_price
    ).filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    return f.render_template('my_goods.html', pagination=pagination)


