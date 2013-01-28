from django.db.models.fields import Field
from django.core.exceptions import ImproperlyConfigured, ValidationError


class ArrayField(Field):
    
    description = """
    PostgreSQL allows columns of a table to be defined as variable-length
    multidimensional arrays. Arrays of any built-in or user-defined base
    type, enum type, or composite type can be created."""
    
    def __init__(self, verbose_name=None, name=None,
                 dimensions=1, data_type=None, **kwargs):
        self.dimensions = dimensions
        self.data_type = data_type
        
        if not type(self.dimensions) == int:
            raise ImproperlyConfigured("ArrayField dimensions must be an integer, but is %s" % self.dimensions)
        if not self.dimensions > 0:
            raise ImproperlyConfigured("ArrayField dimensions must be greater than zero")
        
        if kwargs.get('primary_key'):
            raise ImproperlyConfigured("ArrayField cannot be a primary key.")
        
        if data_type is None:
            raise ImproperlyConfigured("ArrayField requires data_type to be specified.")
        
        Field.__init__(self, verbose_name, name, **kwargs)
    
    def db_type(self, connection):
        return "%s%s" % (self.data_type, "[]" * self.dimensions)
    
    def to_python(self, value):
        if isinstance(value, list):
            return value
        raise ValidationError("ArrayField was expecting a list")