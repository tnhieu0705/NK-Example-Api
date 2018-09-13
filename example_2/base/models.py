from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.IntegerField(null=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    modified_by = models.IntegerField(null=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    deleted_by = models.IntegerField(null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class BaseAbstractUser(AbstractUser):
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.IntegerField(null=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    modified_by = models.IntegerField(null=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    deleted_by = models.IntegerField(null=True)

    class Meta:
        abstract = True
