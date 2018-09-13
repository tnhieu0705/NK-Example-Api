from django.db import models

# Create your models here.
from example_2.base.models import BaseModel
from example_2.categories.models import Category
from example_2.users.models import User


class Product(BaseModel):
    code = models.CharField(max_length=40)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, default='')
    amount = models.PositiveIntegerField(default=0)
    import_price = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'product'
