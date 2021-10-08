#!/usr/bin/python3

from mai import root

# database
SQLALCHEMY_DATABASE_URI = 'sqlite:///mai.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# upload
# max filesize 10mb
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
CSRF_ENABLED = True
UPLOAD_FOLDER = root / 'upload'
UPLOADED_PHOTOS_DEST = UPLOAD_FOLDER / 'img'
for i in UPLOAD_FOLDER, UPLOADED_PHOTOS_DEST:
    if not i.exists():
        i.mkdir()
# safe
SECRET_KEY = '2021'
# bootstrap
BOOTSTRAP_SERVE_LOCAL = True
