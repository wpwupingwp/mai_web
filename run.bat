set FLASK_APP=mai/__init__.py
rem flask db init
rem flask db revision --rev-id xxxxxxxx
flask db migrate
flask db upgrade
python add_data.py
flask run -h 0.0.0.0 -p 2021