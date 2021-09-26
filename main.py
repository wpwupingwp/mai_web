#!/usr/bin/python3

from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <h1>Index</h1>
    <h2>Things</h2>
    <li>lists</li>
    <h2>Users</h2>
    <li>user list</li>'''


@app.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'GET':
        return '''
    <h1>New user</h1>
    <form action="register" method="post">
    <p>Name:<input type="text" name="username"/></p>
    <p>Password:<input type="password" name="password"/></p>
    <br/>
    <input type="submit" value="Submit">
    </form>
    <a href="/register">Register</a>
    '''
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
        return '''
    <h1>Login page</h1>
    <form action="login" method="post">
    <p>Name:<input type="text" name="username"/></p>
    <p>Password:<input type="password" name="password"/></p>
    <br/>
    <input type="submit" value="Submit">
    </form>
    <a href="/register">Register</a>
    '''
    


@app.route('/goods/<int:thing_id>')
def goods(thing_id):
    return render_template('goods.html')


def a():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2021)
