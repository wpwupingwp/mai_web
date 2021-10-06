#!/usr/bin/python3

from pathlib import Path


cwd = Path.cwd().absolute()
SQLALCHEMY_DATABASE_URI = 'sqlite:///mai.db'
UPLOAD_FOLDER = cwd / 'upload'
if not UPLOAD_FOLDER.exists():
    UPLOAD_FOLDER.mkdir()
# max filesize 10mb
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
CSRF_ENABLED = True
SECRET_KEY = '2021'