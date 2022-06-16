# demo-project
Create virtualenv
pipenv --python 3.8
pipenv install

sudo apt-get install postgresql

Create Postgresql Database
sudo su - postges
createdb demo_project


python manage.py migrate
python manage.py createsuperuser

Local run server for debug
pythonn manage.py runserver 0.0.0.0:8000
