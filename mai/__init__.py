#!/usr/bin/python3

from pathlib import Path
from flask import Flask

app = Flask(__name__)
from mai import config
from mai import views
app.secret_key = '2021'
app.config.from_object(config)
app.run(host='0.0.0.0', port=2021)

