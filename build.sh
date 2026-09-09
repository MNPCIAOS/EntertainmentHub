#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py migrate

# This runs your custom setup automatically using variables we will set in Render
python manage.py setup_content_admin
