#!/usr/bin/python3

from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'GET':
        return render_template('login.html', action='register')
    else:
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('user', username=username, password=password))


@app.route('/user/<username>')
def user(username):
    # /templates/user.html
    return render_template('user.html', username=username)


@app.route('/login', methods=('POST', 'GET'))
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('user', username=username, password=password))
    else:
        return render_template('login.html', action='login')


@app.route('/goods/<int:goods_id>')
def goods(goods_id):
    return render_template('goods.html', goods_id=goods_id)


def a():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2021)
