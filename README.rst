Django Pachyderm
================

.. image:: https://secure.travis-ci.org/chrislawlor/django-pachyderm.png
    :alt: Build Status
    :target: http://travis-ci.org/chrislawlor/django-pachyderm.png

A set (well, one for now) of Django Fields for PostgreSQL special data types.

Currently, only ArrayField is supported, but support for JSON and UUID types
is coming soon :)

Why?
----

There are a few other custom field libraries around. Why use Pachyderm?

Well Tested
~~~~~~~~~~~

Pachyderm fields are tested against every version of psycopg2 (from 2.4.1) and the most
two recent releases of Django (currently 1.4 and 1.5).

Note that some features are not supported by all versions of psycopg2. For example,
support array fields of type ``psycopg2.extras.Inet`` was added in psycopg2 2.4.5.


Comprehensive
~~~~~~~~~~~~~

Well, it isn't yet, but will be soon.


Fun
~~~

'Pachyderm' is fun to say :)
