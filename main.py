#!/usr/bin/python3

from flask import Flask, flash, get_flashed_messages,redirect, request, render_template, url_for
from pathlib import Path

import flask
# import flask_mail
# import flask_sqlalchemy
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '2021'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mai.db'
app.config['UPLOAD_FOLDER'] = Path('.').absolute() / 'upload'
if not app.config['UPLOAD_FOLDER'].exists():
    app.config['UPLOAD_FOLDER'].mkdir()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2021)
