from django.db import models
from psycopg2.extras import register_inet

from pachyderm import ArrayField


class NamedModel(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.name


class TextArrayContainer(NamedModel):
    items = ArrayField(dimensions=1, data_type='text')


class IntegerArrayContainer(NamedModel):
    items = ArrayField(dimensions=1, data_type='integer')


register_inet()
class IPArrayContainer(NamedModel):
    items = ArrayField(dimensions=1, data_type='inet')


