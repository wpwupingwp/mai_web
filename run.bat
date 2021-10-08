set FLASK_APP=mai/__init__.py
rem flask db init
rem flask db migrate
python add_data.py
flask run -h 0.0.0.0 -p 2021