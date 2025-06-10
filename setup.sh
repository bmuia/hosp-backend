#!/bin/bash

# install packages
echo "installing packages"
pip install djangorestframework djangorestframework-simplejwt
pip install django-cors-headers
echo "Finished installing necessary packages"

# copy to requirements.txt
echo "freezing to txt"
pip freeze > requirements.txt
echo "finished freezing to txt"

echo "make necessary migrations"
python manage.py makemigrations accounts
python manage.py makemigrations records
python manage.py makemigrations transfers
echo "finished making migrations"

echo "migrate necessary packages"
python manage.py migrate
echo "finished migrating"

echo "hey there Bage🤓, Am pleased to inform you that everything is well setup with no errors. Well done"
echo "best regards"
echo "Belam"
