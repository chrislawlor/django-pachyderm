"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime

from psycopg2.tests.testutils import skip_before_postgres

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, TestCase
from django.db import connection

from .utils import skip_before_psycopg


class AbstractRangeFieldTests(SimpleTestCase):
    
    @skip_before_psycopg('2.5.0')
    def test_missing_kwargs(self):
        from pachyderm.fields.range import AbstractRangeField
        with self.assertRaises(ImproperlyConfigured):
            field = AbstractRangeField(range_class=object)
        with self.assertRaises(ImproperlyConfigured):
            field = AbstractRangeField(range_type='int4range')
    
    @skip_before_psycopg('2.5.0')
    def test_get_prep_value(self):
        from psycopg2.extras import NumericRange
        from pachyderm.fields.range import AbstractRangeField
        field = AbstractRangeField(range_class=NumericRange,
                                   range_type='int4range')
        # should be three-tuple
        with self.assertRaises(ValueError):
            field.get_prep_value((1,2))
        self.assertEqual(NumericRange(1,2,bounds='[]'),
                         field.get_prep_value((1,2,'[]')))

class RangeFieldModelTests(TestCase):
    
    def setUp(self):
        # so we can use 'skip_before_postgres' decorator
        self.conn = connection.cursor().db.connection
        
    @skip_before_postgres(9, 2)
    @skip_before_psycopg('2.5.0')
    def test_date_range_create(self):
        # import models here so it doesn't blow up on postgres < 9.2
        from test_app.models import DateRangeContainer
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        container = DateRangeContainer.objects.create(
            name='container1', span=(today, tomorrow, '[]'))
        self.assertEqual(1, DateRangeContainer.objects.all().count())
