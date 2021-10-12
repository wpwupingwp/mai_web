#!/usr/bin/python3

from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate

from pathlib import Path


app = Flask(__name__)
bootstrap = Bootstrap(app)
lm = LoginManager()
lm.login_view = 'admin.login'
lm.init_app(app)
admin = Admin(app, template_mode='bootstrap4')
root = Path(app.root_path)
app.config.from_pyfile('config.py')

from mai import config
from mai import views
from mai.database import db

migrate = Migrate(app, db)