#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <h1>Index</h1>
    <h2>Things</h2>
    <li>lists</li>
    <h2>Users</h2>
    <li>user list</li>'''



@app.route('/user/<username>')
def user(username):
    return f'''<h1>User profile</h1>
            <p>Username: {username}</p>'''


@app.route('/thing/<int:thing_id>')
def thing(thing_id):
    return f'''<h1>Thing profile</h1>
            <p>Thing ID: {thing_id:06d}</p>'''


def a():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2021)
