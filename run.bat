set FLASK_APP=mai/__init__.py
flask db init
flask db migrate
flask run -h 0.0.0.0 -p 2021