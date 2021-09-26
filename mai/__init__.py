#!/usr/bin/python3

from pathlib import Path
from flask import Flask

app = Flask(__name__)
app.secret_key = '2021'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mai.db'
app.config['UPLOAD_FOLDER'] = Path('.').absolute() / 'upload'
if not app.config['UPLOAD_FOLDER'].exists():
    app.config['UPLOAD_FOLDER'].mkdir()


from mai import views

app.run(host='0.0.0.0', port=2021)

