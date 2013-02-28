# -*- coding: utf-8 -*-
import os
from django.core.exceptions import ImproperlyConfigured

DEBUG = True

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'YOUR_DATABASE'
DATABASE_USER = 'USER'
DATABASE_PASSWORD = 'PASSWORD'


INSTALLED_APPS = (
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.sites',
    'test_app',
)
SITE_ID = 1
ROOT_URLCONF = 'test_project.urls'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

SECRET_KEY = "DON'T MATTER"

try:
    from .local_settings import *
except ImportError:
    raise ImproperlyConfigured("local_settings file is required.")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD
    }
}