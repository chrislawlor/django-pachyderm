# -*- coding: utf-8 -*-
import os
from django.core.exceptions import ImproperlyConfigured

DEBUG = True

def get_env_var(varname, default=None):
    """Get the environment variable or raise an exception."""
    try:
        return os.environ[varname]
    except KeyError:
        if default is not None:
            return default
        raise ImproperlyConfigured("You must set the %s env variable." % varname)

# defaults for TravisCI
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_var('PACHYDERM_DATABASE_NAME', 'pachyderm'),
        'USER': get_env_var('PACHYDERM_DATABASE_USER', 'postgres'),
        'PASSWORD': get_env_var('PACHYDERM_DATABASE_PASSWORD', ''),
    },
}

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



