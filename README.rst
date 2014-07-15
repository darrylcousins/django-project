ujango Project
==============

A test project for django.

Requirements
------------

-  Django ``>=1.7.x``.
-  Python ``3``

Credits
-------

Some of the example models came from the original `django-admin-bootstrapped
<https://github.com/django-admin-bootstrapped/django-admin-bootstrapped>`_
project - namely the ``TestMe`` model.

Installation
------------

Simple install into a virtualenv for testing and evaluation::

    $ git clone https://github.com/darrylcousins/django-project.git
    $ cd django-project

Build Test Project
------------------

The test project uses django-bootstrap3_ and bootstrapped3_ admin along with
`django 1.7 <https://www.djangoproject.com/>`_.  these extra packages can be
installed with::

    $ pip install -r requirements.txt

Run Test Project
----------------

The test project has some tests::

    $ python manage.py test project

The tables, static and sample data can be installed with::

    $ python manage.py migrate
    $ python manage.py loaddata project/fixtures/project.json
    $ python manage.py collectstatic

And can be run with::

    $ python project/manage.py runserver <port>

There are no urls beyond the admin screens and api json views. It attempts to
demonstrate the autocomplete widgets. Login to the admin with ``admin:admin``.
Each of the models demonstrate a different aspect of the bootstrapped3_ admin
and django-autocomplete_ packages.

.. _bootstrapped3: <https://github.com/darrylcousins/django-admin-bootstrapped3>
.. _django-autocomplete: <https://github.com/darrylcousins/django-autocomplete>
.. _django-bootstrap3: <https://github.com/dyve/django-bootstrap3>
