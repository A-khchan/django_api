# django_api

This app is a REST API written in Python, using Django.


Steps to start django server on GCP VM

> cd ~
> source python-venv/bin/activate
> cd django_api/drinks
> nohup python3 manage.py runserver 0.0.0.0:8000 &


After update models.py, goto the directory containing manage.py (ensure u're in v-env)
> cd drinks   (where you found manage.py)
> python3 manage.py makemigrations
> python3 manage.py migrate




Steps to start django server on local MacBook

> cd ~/Documents/App/django_api
> source python-venv/bin/activate
> cd drinks
> python3 manage.py runserver 0.0.0.0:8000 


How to view sqlite data
> 