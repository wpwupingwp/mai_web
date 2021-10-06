#!/usr/bin/python3

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import flask_uploads

from pathlib import Path


app = Flask(__name__)
bootstrap = Bootstrap(app)
lm = LoginManager()
lm.login_view = 'admin.login'
lm.init_app(app)

photos = flask_uploads.UploadSet('photos', flask_uploads.IMAGES)
root = Path(app.root_path)
app.config.from_pyfile('config.py')
flask_uploads.configure_uploads(app, (photos, ))

from mai import config
from mai import views

app.run(host='0.0.0.0', port=2021)
