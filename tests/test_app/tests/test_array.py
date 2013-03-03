"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.test import TransactionTestCase, SimpleTestCase

from pachyderm.fields import (
    CharacterArrayField,
    IntegerArrayField,
)

from pachyderm.fields.array import AbstractArrayField

from test_app.models import (
    BooleanArrayContainer,
    CharArrayContainer,
    IntegerArrayContainer,
)

from .utils import skip_before_psycopg


class AbstractArrayFieldTests(SimpleTestCase):
    def test_zero_dimensions(self):
        with self.assertRaises(ImproperlyConfigured):
            field = AbstractArrayField(dimensions=0, data_type='test')
    
    def test_missing_data_type(self):
        with self.assertRaises(ImproperlyConfigured):
            field = AbstractArrayField()
            
    def test_no_pk(self):
        with self.assertRaises(ImproperlyConfigured):
            field = AbstractArrayField(primary_key=True, data_type='test')
    
    def test_non_integer_dimensions(self):
        with self.assertRaises(ImproperlyConfigured):
            field = AbstractArrayField(dimensions='one', data_type='test')
    
    def test_db_type(self):
        field = AbstractArrayField(dimensions=2, data_type='test')
        self.assertEqual('test[][]', field.db_type(object))
    
    def test_description(self):
        field = AbstractArrayField(data_type='test')
        self.assertEqual("PostgreSQL array field of type test.",
                         field.description)
    
    def test_get_prep_value(self):
        field = AbstractArrayField(data_type='test')
        with self.assertRaises(ValueError):
            field.get_prep_value('not a list')
    
    def test_to_python(self):
        field = AbstractArrayField(data_type='test')
        with self.assertRaises(ValidationError):
            field.to_python('not a list')


class CharacterArrayFieldTests(SimpleTestCase):
    def test_missing_max_length(self):
        with self.assertRaises(ImproperlyConfigured):
            field = CharacterArrayField()
    
    def test_non_integer_max_length(self):
        with self.assertRaises(ImproperlyConfigured):
            field = CharacterArrayField(max_length='ten')


class ArrayFieldModelTests(TransactionTestCase):
    def test_adding_rows(self):
        container = CharArrayContainer.objects.create(
            name='django', items=['framework', 'python'])
        self.assertEqual(1, CharArrayContainer.objects.all().count())
        retrieved = CharArrayContainer.objects.get(name='django')
        self.assertEqual(container.items, retrieved.items)
        self.assertEqual(2, len(retrieved.items))
        self.assertEqual(container.items[0], retrieved.items[0])
        self.assertEqual(container.items[1], retrieved.items[1])

    def test_contains_array_element(self):
        CharArrayContainer.objects.create(
            name='django', items=['framework', 'python'])
        self.assertEqual(1, CharArrayContainer.objects.filter(
            items__contains='framework').count())
        self.assertEqual(0, CharArrayContainer.objects.filter(
            items__contains='php').count())
    
    def test_boolean_type(self):
        container = BooleanArrayContainer(name='container',
                                          items=[True, False])
        container.save()
        self.assertEqual(1, BooleanArrayContainer.objects.all().count())
        retrieved = BooleanArrayContainer.objects.get(name='container')
        self.assertEqual(container.items, retrieved.items)
        container2 = BooleanArrayContainer(name='container2',
                                           items=[False, False])
        container2.save()
        self.assertEqual(2, BooleanArrayContainer.objects.all().count())

    def test_integer_type(self):
        container = IntegerArrayContainer.objects.create(
            name='container', items=[1, 2, 3, 4, 5])
        self.assertEqual(1, IntegerArrayContainer.objects.all().count())
        retrieved = IntegerArrayContainer.objects.get(name='container')
        self.assertEqual(container.items, retrieved.items)
        self.assertEqual(5, len(retrieved.items))
        self.assertEqual(1, IntegerArrayContainer.objects.filter(
            items__contains=1).count())
    
    def test_contains_uses_one_query(self):
        container1 = IntegerArrayContainer.objects.create(
            name='container1', items=[1, 2, 3, 4, 5])
        container2 = IntegerArrayContainer.objects.create(
            name='container2', items=[5, 6, 7, 8, 9])
        with self.assertNumQueries(1):
            retrieved = list(IntegerArrayContainer.objects.filter(items__contains=5))
        self.assertEqual(2, len(retrieved))
        
    @skip_before_psycopg('2.4.5')
    def test_inet_type(self):
        from test_app.models import IPArrayContainer
        container = IPArrayContainer.objects.create(
            name='server1', items=['10.10.10.10', '10.10.10.11'])
        self.assertEqual(1, IPArrayContainer.objects.all().count())
        retrieved = IPArrayContainer.objects.get(name='server1')
        self.assertEqual('10.10.10.10', retrieved.items[0])
