#!/usr/bin/python3

import flask as f

# import flask_mail

from mai import app, lm, root
from mai.database import User, Goods, Bid, db
from mai.admin import admin


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


@app.route('/goods')
@app.route('/goods/<int:page>')
def goods(page=1):
    per_page = 5
    pagination = Goods.query.paginate(page=page, per_page=per_page)
    return f.render_template('goods.html', pagination=pagination)


@app.route('/user')
@app.route('/user/<int:page>')
def user(page=1):
    per_page = 5
    pagination = User.query.paginate(page=page, per_page=per_page)
    return f.render_template('user.html', pagination=pagination)


@app.route('/user/<username>')
def manage_user(username):
    # /templates/user.html
    return f.render_template(
        'user.html', users=User.query.filter_by(username=username).all())


app.register_blueprint(admin, url_prefix='/admin')
