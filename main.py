#!/usr/bin/python3

from pathlib import Path

import flask as f
from werkzeug.utils import secure_filename

# import flask_mail
# import flask_sqlalchemy

global app
app = f.Flask(__name__)
app.secret_key = '2021'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mai.db'
app.config['UPLOAD_FOLDER'] = Path('.').absolute() / 'upload'
if not app.config['UPLOAD_FOLDER'].exists():
    app.config['UPLOAD_FOLDER'].mkdir()



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
        return f.redirect(f.url_for('user', username=username,
                                    password=password))


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


# db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    # email
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    register_date = db.Column(db.DateTime)
    address = db.Column(db.String(100))
    bider_id = db.relationship('Bid', backref='user')

    def __init__(self, username, password, address):
        self.username = username
        self.password = password
        self.register_date = datetime.utcnow()
        self.address = address

    def __repr__(self):
        return f'{self.username}'


class Goods(db.Model):
    goods_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # address for delivery
    address = db.Column(db.String(100))
    no_bid = db.Column(db.Boolean)
    description = db.Column(db.Text)
    highest_price = db.Column(db.Float)
    lowest_price = db.Column(db.Float)
    pub_date = db.Column(db.DateTime)
    expired_date = db.Column(db.DateTime)
    photo1 = db.Column(db.LargeBinary)
    photo2 = db.Column(db.LargeBinary)
    photo3 = db.Column(db.LargeBinary)
    # ?
    goods = db.relationship('Bid', backref='goods')


class Bid(db.Model):
    bid_id = db.Column(db.Integer, primary_key=True)
    bider_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.goods_id'))
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2021)
