try:
    import simplejson as json
except ImportError:
    import json

from django.db import models
from django.utils import six

import psycopg2.extras

if hasattr(psycopg2.extras, 'Json'):
    from psycopg2.extras import Json


    class JSONField(six.with_metaclass(models.SubfieldBase, models.Field)):
        description = """PostgreSQL JSON field."""
        
        def db_type(self, connection):
            return "json"
        
        def get_prep_value(self, value):
            return Json(value)
        
        def to_python(self, value):
            if isinstance(value, dict):
                return value
            return json.loads(value)
    