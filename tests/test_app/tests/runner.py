"""https://github.com/jezdez/django-discover-runner"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase


from django.utils.importlib import import_module

try:
    from django.utils.unittest import defaultTestLoader
except ImportError:
    try:
        from unittest2 import defaultTestLoader  # noqa
    except ImportError:
        raise ImproperlyConfigured("Couldn't import unittest2 default "
                                   "test loader. Please use Django >= 1.3 "
                                   "or install the unittest2 library.")


try:
    from django.test.runner import DiscoverRunner
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner, reorder_suite

    class DiscoverRunner(DjangoTestSuiteRunner):
        """
        A test suite runner that uses unittest2 test discovery.


        """
        def build_suite(self, test_labels, extra_tests=None, **kwargs):
            suite = None
            root = getattr(settings, 'TEST_DISCOVER_ROOT', '.')
            top_level = getattr(settings, 'TEST_DISCOVER_TOP_LEVEL', None)
            pattern = getattr(settings, 'TEST_DISCOVER_PATTERN', 'test*.py')

            if test_labels:
                suite = defaultTestLoader.loadTestsFromNames(test_labels)
                # if single named module has no tests, do discovery within it
                if not suite.countTestCases() and len(test_labels) == 1:
                    suite = None
                    root = import_module(test_labels[0]).__path__[0]

            if suite is None:
                suite = defaultTestLoader.discover(root,
                    pattern=pattern, top_level_dir=top_level)

            if extra_tests:
                for test in extra_tests:
                    suite.addTest(test)

            return reorder_suite(suite, (TestCase,))
