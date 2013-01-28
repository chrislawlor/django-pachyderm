from django.db import models
from pachyderm import ArrayField


class Item(models.Model):
    name = models.CharField(max_length=20)
    tags = ArrayField(dimensions=1, data_type='text')
    
    def __unicode__(self):
        return self.name
