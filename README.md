#### Segna Ore

A system for annotate your worked hours.


# Requirements

Python => 3.6

for mysql install libmysqlclient-dev. For Debian based system use:

$ sudo apt-get install libmysqlclient-dev

# Installation

- Create a virtualenv

- Install required modules
$ pip install -r requirements.txt

- Create your configuration file and populate it with your settings. Eg.:

$ cp settings/sample.py settings/local.py

- Run migrations

$ (venv) python manage.py migrate --settings=settings.local

- You can create a superuser from shell

$ (venv) python manage.py createsuperuser --settings=settings.local

- Run the local server:

$ (venv) python manage.py runserver 8081 --settings=settings.local

- or use the shortcut:

$ (venv) bash runserver.sh

# Contact me

Fluidone

morin@fluidone.it
