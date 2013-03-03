import uuid

from django.db import models
from django.utils import six
from django.core.exceptions import ImproperlyConfigured

import psycopg2
from psycopg2.extras import register_uuid, UUID_adapter

# TODO: Shouldn't call this unless the field is used
register_uuid()

class UUIDField(six.with_metaclass(models.SubfieldBase, models.Field)):
    description = """
    Python UUID field. If used as a primary key, will automatically
    generate v1 UUIDs.
    """
    
    def db_type(self, connection):
        return "uuid"
    
    def pre_save(self, model_instance, add):
        current_val = getattr(model_instance, self.attname, None)
        if self.primary_key and add:
            if current_val is None:
                current_val = uuid.uuid1()
        return current_val
    
    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            #return psycopg2.extensions.adapt(value).getquoted()
            return value
        raise ValueError("UUIDField expects a UUID or None")
    
    def to_python(self, value):
        if not value:
            return None
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value
    
    def contribute_to_class(self, cls, name):
        if self.primary_key:
            assert not cls._meta.has_auto_field, \
                   "A model can't have more than one AutoField."
            super(UUIDField, self).contribute_to_class(cls, name)
            cls._meta.has_auto_field = True
            cls._meta.auto_field = self
        else:
            super(UUIDField, self).contribute_to_class(cls, name) 