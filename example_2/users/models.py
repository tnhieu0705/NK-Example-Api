from django.db import models


# Create your models here.
from example_2.base.constants.common import AppConstants
from example_2.base.models import BaseAbstractUser


class User(BaseAbstractUser):
    phone = models.CharField(blank=True, default='', max_length=30)
    role_id = models.IntegerField(default=AppConstants.Role.User)
    image_url = models.CharField(max_length=200, default='', blank=True)

    class Meta:
        db_table = 'user'


class Login(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
