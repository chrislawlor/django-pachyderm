from django.db import models
from django.utils import six
from django.core.exceptions import ImproperlyConfigured

import psycopg2.extras

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
