#!/usr/bin/python3

from pathlib import Path

import flask as f
from werkzeug.utils import secure_filename

# import flask_mail
# import flask_sqlalchemy

from mai import app
from mai.database import *
from mai.form import UserForm, GoodsForm


@app.route('/')
@app.route('/index')
def index():
    return f.render_template('index.html')


@app.route('/register', methods=('POST', 'GET'))
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


@app.route('/add_goods', methods=('POST', 'GET'))
def add_goods():
    gf = GoodsForm()
    if gf.validate_on_submit():
        goods = Goods(gf)
        db.session.add(goods)
        db.session.commit()
        f.flash('添加物品成功')
        print('ok')
        return f.redirect('goods')
    return f.render_template('add_goods.html', form=gf)


@app.route('/goods')
def goods():
    # ? add paginate
    return f.render_template('add_goods.html', goods=Goods.query.all())


@app.route('/user/<username>')
def user(username):
    # /templates/user.html
    return f.render_template(
        'user.html', users=User.query.filter_by(username=username).all())


@app.route('/user')
def manage_user():
    return f.render_template('user.html', users=User.query.all())


@app.route('/login', methods=('POST', 'GET'))
def admin():
    error = None
    if f.request.method == 'POST':
        username = f.request.form['username']
        password = f.request.form['password']
        if username.startswith('error'):
            error = 'bad username'
        else:
            f.flash('OK')
        print(error)
        return f.redirect(f.url_for('user', username=username, password=password))
    else:
        return f.render_template('login.html', action='login', error=error)




@app.route('/upload', methods=('GET', 'POST'))
def upload_file():
    if f.request.method == 'POST':
        file = f.request.files['file']
        print(file.name)
        file.save(app.config['UPLOAD_FOLDER']/secure_filename(file.name))
        return 'Upload ok'
    return f.render_template('upload.html')