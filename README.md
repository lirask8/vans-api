#### Technologies

  * [Django](https://www.djangoproject.com/)
  * [Django Rest Framework](http://www.django-rest-framework.org/)

You need to have installed `git`, `docker`, `ssh`.

#### Basic commands for running project
  * `docker-compose build` build the images for development.
  * `docker-compose run web python manage.py createsuperuser` create a superuser
  * `docker-compose run web python manage.py loaddata users status vans` load fixtures
  * `docker-compose up` run the server
  * `docker-compose run web python manage.py test` run the tests


#### Other functional commands
  * `docker-compose run --service-ports web` Debug console
  * `docker-compose run web python manage.py makemigrations` make the migrations
  * `docker-compose run web python manage.py migrate` apply the migrations
  * `docker-compose run web python manage.py makemessages` make messages for translations
  * `docker-compose run web python manage.py compilemessages` compile messages for translations
  * `docker-compose run web python manage.py dumpdata vans.status > fixtures/status.json` dump fixtures


### Run django admin and mailhog ui

* [http://localhost:8000/admin/](http://localhost:8000/admin/)
* [http://localhost:8025/#](http://localhost:8025/#)



## Getting started without Docker

### Install linux dependencies

```shell
sudo apt-get install libpq-dev python-dev python3-dev postgresql postgresql-contrib python-virtualenv python-pip

```

### Virtualenv configuration

Create a new virtualenv

```shell
virtualenv -p /usr/bin/python3  virtualenvname

```

Activate the virtualenv 

```shell

source /path/to/yourVirtualenv/virtualenvName/bin/activate

```

Install dependencies into virtualenv

under the project folder install requirements with pip (activate the virtualenv before install dependences)

```shell
pip install -r requirements.txt
```

### Collect statics files

collect static files  with `python manage.py collectstatic`


### Apply migrations

```shell
python manage.py migrate

```

### Create a super user for django admin

```shell
python manage.py createsuperuser

```

#### Run the project

Run  it with testing server

```shell
python manage.py runserver 0.0.0.0:(port)

```