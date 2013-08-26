from psycopg2.tests.testutils import skip_before_postgres

from django.test import TestCase
from django.db import connection

from .utils import skip_before_psycopg


class JSONFieldTests(TestCase):
    
    def setUp(self):
        # so we can use 'skip_before_postgres' decorator
        self.conn = connection.cursor().db.connection
    
    @skip_before_psycopg('2.5.0')
    @skip_before_postgres(9, 2)
    def test_db_type(self):
        from pachyderm.fields import JSONField
        field = JSONField()
        self.assertEqual('json', field.db_type(object))
    
    @skip_before_psycopg('2.5.0')
    @skip_before_postgres(9, 2)
    def test_create_from_dict(self):
        from test_app.models import JSONContainer
        data = {'one': 1, 'two': 2}
        container = JSONContainer.objects.create(name='container',
                                                 json=data)
        self.assertEqual(1, JSONContainer.objects.all().count())
        retrieved = JSONContainer.objects.get(name='container')
        self.assertEqual(data, retrieved.json)
        self.assertTrue(isinstance(retrieved.json, dict))
        self.assertEqual(1, retrieved.json['one'])
        self.assertEqual(2, retrieved.json['two'])
    
    @skip_before_psycopg('2.5.0')
    @skip_before_postgres(9, 2)
    def test_create_from_str(self):
        from test_app.models import JSONContainer
        import json
        data = {'one': 1, 'two': 2}
        container = JSONContainer.objects.create(name='container',
                                                 json=json.dumps(data))
        self.assertEqual(1, JSONContainer.objects.all().count())
        retrieved = JSONContainer.objects.get(name='container')
        self.assertEqual(data, retrieved.json)
        self.assertTrue(isinstance(retrieved.json, dict))

    @skip_before_psycopg('2.5.0')
    @skip_before_postgres(9, 2)
    def test_direct_access(self):
        from test_app.models import JSONContainer
        data = {'foo': 'bar'}
        container = JSONContainer.objects.create(name='container',
                                                 json=data)
        container.json['foo'] = 'baz'
        container.save()
        retrieved = JSONContainer.objects.get(name='container')
        self.assertEqual('baz', retrieved.json['foo'])
