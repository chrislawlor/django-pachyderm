from django.db import models
from django.utils import six
from django.core.exceptions import ImproperlyConfigured, ValidationError

import psycopg2.extras


class AbstractArrayField(six.with_metaclass(models.SubfieldBase,
                                            models.Field)):
    def __init__(self, verbose_name=None, name=None,
                 dimensions=1, data_type=None, **kwargs):
        self.dimensions = dimensions
        self.data_type = data_type

        if not type(self.dimensions) == int:
            raise ImproperlyConfigured(
                "ArrayField dimensions must be an integer, but is %s"
                % type(self.dimensions))

        if not self.dimensions > 0:
            raise ImproperlyConfigured(
                "ArrayField dimensions must be greater than zero")

        if kwargs.get('primary_key'):
            raise ImproperlyConfigured(
                "ArrayField cannot be a primary key.")

        if data_type is None:
            raise ImproperlyConfigured(
                "ArrayField requires data_type to be specified.")

        models.Field.__init__(self, verbose_name, name, **kwargs)

    @property
    def description(self):
        return "PostgreSQL array field of type %s." % self.data_type

    def db_type(self, connection):
        return "%s%s" % (self.data_type, "[]" * self.dimensions)

    def get_prep_value(self, value):
        if not isinstance(value, list):
            raise ValueError(
                "%s was expecting a list" % self.__class__.__name__)
        return value

    def to_python(self, value):
        if isinstance(value, list):
            return value
        raise ValidationError("ArrayField was expecting a list")


class IntegerArrayField(AbstractArrayField):
    def __init__(self, *args, **kwargs):
        kwargs['data_type'] = 'integer'
        super(IntegerArrayField, self).__init__(*args, **kwargs)


class CharacterArrayField(AbstractArrayField):
    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            raise ImproperlyConfigured(
                "CharacterArrayField requires the max_length kwarg")
        max_length = kwargs.pop('max_length')
        if not isinstance(max_length, int):
            raise ImproperlyConfigured(
                "max_length must be an integer")
        kwargs['data_type'] = 'varchar(%d)' % max_length
        super(CharacterArrayField, self).__init__(*args, **kwargs)


class BooleanArrayField(AbstractArrayField):
    def __init__(self, *args, **kwargs):
        kwargs['data_type'] = 'bool'
        super(BooleanArrayField, self).__init__(*args, **kwargs)


if hasattr(psycopg2.extras, 'Inet'):
    # This is a little off... Inet existed before support for
    # Inet arrays...
    from psycopg2.extras import Inet, register_inet

    # We shouldn't call this unless the field is actually being used
    register_inet()

    class IPArrayField(AbstractArrayField):
        def __init__(self, *args, **kwargs):
            kwargs['data_type'] = 'inet'
            super(IPArrayField, self).__init__(*args, **kwargs)

        def get_prep_value(self, value):
            super(IPArrayField, self).get_prep_value(value)
            return [Inet(addr) for addr in value]

        def to_python(self, value):
            super(IPArrayField, self).to_python(value)
            result = []
            for inet in value:
                if type(inet) is Inet:
                    result.append(inet.addr)
                else:
                    result.append(inet)
            return result

if hasattr(psycopg2.extras, 'Range'):
    from psycopg2.extras import (
        NumericRange,
        DateRange,
        DateTimeRange,
        DateTimeTZRange,
    )

    class AbstractRangeField(six.with_metaclass(models.SubfieldBase,
                                                models.Field)):
        def __init__(self, verbose_name=None, name=None,
                     range_type=None, range_class=None, **kwargs):
            if range_type is None:
                raise ImproperlyConfigured(
                    "RangeField requires range_type to be specified.")
            if range_class is None:
                raise ImproperlyConfigured(
                    "RangeField requires a range_class to be specified.")
            self.range_type = range_type
            self.range_class = range_class

            models.Field.__init__(self, verbose_name, name, **kwargs)

        def db_type(self, connection):
            return self.range_type

        def get_prep_value(self, value):
            # `value` should be a three-tuple
            if not len(value) == 3:
                raise ValueError("range must be a three-tuple")
            return self.range_class(value[0], value[1], bounds=value[2])


    class IntegerRangeField(AbstractRangeField):
        def __init__(self, *args, **kwargs):
            kwargs['range_type'] = 'int4rage'
            kwargs['range_class'] = NumericRange
            super(IntegerRangeField, self).__init__(*args, **kwargs)


    class BigIntegerRangeField(AbstractRangeField):
        def __init__(self, *args, **kwargs):
            kwargs['range_type'] = 'int8range'
            kwargs['range_class'] = NumericRange
            super(BigIntegerRangeField, self).__init__(*args, **kwargs)


    class NumericRangeField(AbstractRangeField):
        def __init__(self, *args, **kwargs):
            kwargs['range_type'] = 'numrange'
            kwargs['range_class'] = NumericRange
            super(NumericRangeField, self).__init__(*args, **kwargs)


    class TimestampRangeField(AbstractRangeField):
        def __init__(self, *args, **kwargs):
            kwargs['range_type'] = 'tsrange'
            kwargs['range_class'] = DateTimeRange
            super(TimestampRangeField, self).__init__(*args, **kwargs)


    class TimstampTZRangeField(AbstractRangeField):
        def __init__(self, *args, **kwargs):
            kwargs['range_type'] = 'tstzrange'
            kwargs['range_class'] = DateTimeTZRange
            super(TimstampTZRangeField, self).__init__(*args, **kwargs)


    class DateRangeField(AbstractRangeField):
        def __init__(self, *args, **kwargs):
            kwargs['range_type'] = 'daterange'
            kwargs['range_class'] = DateRange
            super(DateRangeField, self).__init__(*args, **kwargs)
