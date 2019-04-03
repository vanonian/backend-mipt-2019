#!/bin/sh
export FLASK_APP=first_app.py
flask db init
flask db migrate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - first_app:app
