from example_2.payments.models import Vendor
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *


class OrderDetailProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'amount', 'import_price', 'price', 'is_active']


class CreateProductSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=40, required=False, allow_blank=True)
    name = serializers.CharField(max_length=254, validators=[UniqueValidator(queryset=Product.objects.all())])
    description = serializers.CharField(required=False, default='')
    amount = serializers.IntegerField(default=0)
    import_price = serializers.DecimalField(max_digits=9, decimal_places=0, default=0)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(deleted_at=None), required=False, allow_null=True)
    vendor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role_id=4, deleted_at=None), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'amount', 'import_price', 'price', 'is_active', 'category', 'vendor']


class RetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(required=False, default='')
    amount = serializers.IntegerField(required=False, default=0)
    import_price = serializers.DecimalField(required=False, max_digits=9, decimal_places=0, default=0)
    is_active = serializers.BooleanField(required=False, default=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(deleted_at=None), required=False, allow_null=True)
    vendor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role_id=4, deleted_at=None), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'amount', 'import_price', 'price', 'is_active', 'category', 'vendor']


# VENDOR
class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id', 'stripe_id']
