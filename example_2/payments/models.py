from django.db import models

from example_2.users.models import User


# Create your models here.
class StripeObject(models.Model):
    stripe_id = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        abstract = True


class Customer(StripeObject):
    user = models.OneToOneField(User, null=True, related_name='customer', on_delete=models.CASCADE)

    class Meta:
        db_table = 'customer'


class Vendor(StripeObject):
    user = models.OneToOneField(User, null=True, related_name='vendor', on_delete=models.CASCADE)
    address = models.CharField(max_length=150, default='VN')

    class Meta:
        db_table = 'vendor'


class Card(StripeObject):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = 'card'


class Charge(StripeObject):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=0, max_digits=10, default=0)
    currency = models.CharField(max_length=7, default="usd")

    class Meta:
        db_table = 'charge'
