"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import unittest

import psycopg2
from psycopg2.extras import Inet

from django.test import TransactionTestCase
from django.db import DatabaseError

from .models import TextArrayContainer, IntegerArrayContainer, IPArrayContainer


def psycopg2_version_gte(version_string):
    version = psycopg2.__version__[:5]
    return version >= version_string


class ArrayFieldTests(TransactionTestCase):
    def test_adding_rows(self):
        container = TextArrayContainer.objects.create(
            name='django', items=['framework', 'python'])
        self.assertEqual(1, TextArrayContainer.objects.all().count())
        retrieved = TextArrayContainer.objects.get(name='django')
        self.assertEqual(container.items, retrieved.items)
        self.assertEqual(2, len(retrieved.items))
        self.assertEqual(container.items[0], retrieved.items[0])
        self.assertEqual(container.items[1], retrieved.items[1])

    def test_contains_array_element(self):
        TextArrayContainer.objects.create(
            name='django', items=['framework', 'python'])
        self.assertEqual(1, TextArrayContainer.objects.filter(
            items__contains='framework').count())
        self.assertEqual(0, TextArrayContainer.objects.filter(
            items__contains='php').count())

    def test_integer_type(self):
        container = IntegerArrayContainer.objects.create(
            name='container', items=[1, 2, 3, 4, 5])
        self.assertEqual(1, IntegerArrayContainer.objects.all().count())
        retrieved = IntegerArrayContainer.objects.get(name='container')
        self.assertEqual(container.items, retrieved.items)
        self.assertEqual(5, len(retrieved.items))
        self.assertEqual(1, IntegerArrayContainer.objects.filter(
            items__contains=1).count())

    @unittest.skipUnless(psycopg2_version_gte('2.4.5'),
                         'Array support for Inet introduced in psycopg2 2.4.5')
    def test_inet_type(self):
        container = IPArrayContainer.objects.create(
            name='server1', items=[Inet('10.10.10.10'), Inet('10.10.10.11')])
        self.assertEqual(1, IPArrayContainer.objects.all().count())
        retrieved = IPArrayContainer.objects.get(name='server1')
        # psycopg2's Inet does not support direct comparisons, i.e.
        # Inet('10.10.10.10') == Inet('10.10.10.10') is False
        self.assertEqual('10.10.10.10', retrieved.items[0].addr)
