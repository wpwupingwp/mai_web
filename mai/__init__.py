#!/usr/bin/python3

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
bootstrap = Bootstrap(app)
lm = LoginManager()
lm.login_view = 'admin.login'
lm.init_app(app)

from mai import config
from mai import views
app.secret_key = '2021'
app.config.from_pyfile('config.py')
app.run(host='0.0.0.0', port=2021)

