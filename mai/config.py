#!/usr/bin/python3

from pathlib import Path


SQLALCHEMY_DATABASE_URI = 'sqlite:///mai.db'
UPLOAD_FOLDER = Path('.').absolute() / 'upload'
if not UPLOAD_FOLDER.exists():
    UPLOAD_FOLDER.mkdir()