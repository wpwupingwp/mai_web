#!/usr/bin/python3

from pathlib import Path


cwd = Path.cwd().absolute()
SQLALCHEMY_DATABASE_URI = 'sqlite:///mai.db'
UPLOAD_FOLDER = cwd / 'upload'
if not UPLOAD_FOLDER.exists():
    UPLOAD_FOLDER.mkdir()
CSRF_ENABLED = True
SECRET_KEY = '2021'