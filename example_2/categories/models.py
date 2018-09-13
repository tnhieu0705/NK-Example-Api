from django.db import models

from example_2.base.models import BaseModel


# Create your models here.
class Category(BaseModel):
    code = models.CharField(max_length=40)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150, blank=True, default='')

    class Meta:
        db_table = 'category'
