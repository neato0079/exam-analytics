#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Update DB with migrations

python manage.py makemigrations
python manage.py migrate