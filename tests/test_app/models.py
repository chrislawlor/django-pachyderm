from django.db import models

from pachyderm.fields import (
    CharacterArrayField,
    IntegerArrayField,
    BooleanArrayField,
    UUIDField
)

from .tests.utils import postgres_version_gte, psycopg2_version_gte


class NamedModel(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.name


class CharArrayContainer(NamedModel):
    items = CharacterArrayField(max_length=10)


class IntegerArrayContainer(NamedModel):
    items = IntegerArrayField()
    

class BooleanArrayContainer(NamedModel):
    items = BooleanArrayField()


if psycopg2_version_gte('2.4.5'):
    from pachyderm.fields import IPArrayField
    class IPArrayContainer(NamedModel):
        items = IPArrayField()

# Range field models

if postgres_version_gte(9,2) and psycopg2_version_gte('2.5.0'):
    from pachyderm.fields import DateRangeField
    
    class DateRangeContainer(NamedModel):
        span = DateRangeField()


# UUIDField models

class UUIDContainerNonPK(NamedModel):
    uuid = UUIDField()

class UUIDContainerPK(NamedModel):
    id = UUIDField(primary_key=True)

