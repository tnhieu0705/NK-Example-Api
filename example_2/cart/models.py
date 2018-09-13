from django.db import models
from example_2.base.constants.common import AppConstants

from example_2.products.models import Product
from example_2.base.models import BaseModel
from example_2.users.models import User


# Create your models here.
class Order(BaseModel):
    total_amount = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    status = models.IntegerField(default=AppConstants.RoleOrder.Cart)
    checked_out = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'order'


class OrderDetail(BaseModel):
    order = models.ForeignKey(Order, related_name='order_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_detail', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'order_detail'
