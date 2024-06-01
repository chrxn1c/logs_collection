#!/bin/sh

poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run gunicorn --workers=1 -b=0.0.0.0:$PORT general.wsgi:application