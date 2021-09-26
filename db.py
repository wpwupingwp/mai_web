#!/usr/bin/python3

from flask_sqlalchemy import SQLAlchemy

from main import app


db = SQLAlchemy(app)