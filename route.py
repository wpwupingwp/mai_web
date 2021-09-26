#!/usr/bin/python3

import flask as f
from werkzeug.utils import secure_filename

from main import app


@app.route('/')
def index():
    return f.render_template('index.html')


@app.route('/register', methods=('POST', 'GET'))
def register():
    if f.request.method == 'GET':
        return f.render_template('login.html', action='register')
    else:
        username = f.request.form['username']
        password = f.request.form['password']
        return f.redirect(f.url_for('user', username=username, password=password))


@app.route('/user/<username>')
def user(username):
    # /templates/user.html
    return f.render_template('user.html', username=username)


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


@app.route('/goods/<int:goods_id>')
def goods(goods_id):
    return f.render_template('goods.html', goods_id=goods_id)


@app.route('/upload', methods=('GET', 'POST'))
def upload_file():
    if f.request.method == 'POST':
        file = f.request.files['file']
        print(file.name)
        file.save(app.config['UPLOAD_FOLDER']/secure_filename(file.name))
        return 'Upload ok'
    return f.render_template('upload.html')
