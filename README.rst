Django Pachyderm
================

.. image:: https://secure.travis-ci.org/chrislawlor/django-pachyderm.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/chrislawlor/django-pachyderm

A set of Django Fields for PostgreSQL special data types.


JSON
----

Deal directly with ``dict`` objects. Don't manually serialize to strings::

    from pachyderm.fields import JSONField


	class MyModel(models.Model):
		data = JSONField()

	>>> instance = MyModel.objects.create(data={'foo': bar})
	>>> type(instance.data)
	dict


UUID
----

UUIDs make great primary keys::


    from pachyderm.fields import UUIDField


	class MyModel(models.Model):
	    pk = UUIDField(primary_key=True)


	>>> instance = MyModel()
	>>> instance.save()
	>>> type(instance.id)
	uuid.UUID


ArrayField
----------

Easily work with multi-dimensional arrays without seriializing to strings::

	class MyModel(models.Model):
	    matrix = IntegerArrayField(dimensions=2)

	>>> instance = MyModel.objects.create(matrix=[[1, 0], [0, 1]])
	>>> type(instance.matrix)
	list
	>>> instance.matrix[0]
	[1, 0]

Currently, ArrayField, UUIDField, and JSONField are supported, and support for
range fields is coming soon :)

Why?
----

There are a few other custom field libraries around. Why use Pachyderm?

Well Tested
~~~~~~~~~~~

Pachyderm fields are tested against every version of psycopg2 (from 2.4.1) and the most
two recent releases of Django (currently 1.4 and 1.5).

Note that some features are not supported by all versions of psycopg2 and / or
PostgreSQL. For example, support for array fields of type ``psycopg2.extras.Inet`` 
was added in psycopg2 2.4.5, and support for JSON fields was added in PostgreSQL
9.2.

Also, Pachyderm is tested against Python 2.6, 2.7, 3.2, and 3.3.


Comprehensive
~~~~~~~~~~~~~

Well, it isn't yet, but will be soon.


Fun
~~~

'Pachyderm' is fun to say :)
