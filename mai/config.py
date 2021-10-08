#!/usr/bin/python3

from mai import root


SQLALCHEMY_DATABASE_URI = 'sqlite:///mai.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# max filesize 10mb
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
CSRF_ENABLED = True
SECRET_KEY = '2021'
UPLOAD_FOLDER = root / 'upload'
UPLOADED_PHOTOS_DEST = UPLOAD_FOLDER / 'img'
for i in UPLOAD_FOLDER, UPLOADED_PHOTOS_DEST:
    if not i.exists():
        i.mkdir()
