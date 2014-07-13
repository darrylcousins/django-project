Django Project
==============

A test project for django.

Installation
------------

Simple install into a virtualenv for testing and evaluation::

    $ git clone https://github.com/darrylcousins/django-project.git
    $ cd django-project
    $ python setup.py develop

Run Tests
---------

Run the tests::

    $ python runtests.py

Build and Run Test Project
--------------------------

The test project uses django-bootstrap3_ and bootstrapped3_ admin.  these extra
packages can be installed with::

    $ pip install -r requirements.txt

The test project has some tests::

    $ python manage.py test project

The tables, static and sample data can be installed with::

    $ python manage.py collectstatic
    $ python manage.py migrate
    $ python manage.py loaddata project/fixtures/project.json

And can be run with::

    $ python project/manage.py runserver 9000

There are no urls beyond the admin screens and api json views. It attempts to
demonstrate the autocomplete widgets.

.. _bootstrapped3: <https://github.com/darrylcousins/django-admin-bootstrapped3>
.. _django-bootstrap3: <https://github.com/dyve/django-bootstrap3>
