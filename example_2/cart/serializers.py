from example_2.cart.models import OrderDetail, Order
from example_2.products.serializers import OrderDetailProductSerializer
from example_2.users.serializers import UserSerializer
from rest_framework import serializers


class OrderDetailSerializer(serializers.ModelSerializer):
    product = OrderDetailProductSerializer(many=False, read_only=True)

    class Meta:
        model = OrderDetail
        fields = ['id', 'order', 'product', 'quantity', 'unit_price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'checked_out', 'total_amount', 'total_price', 'status', 'owner', 'order_detail']


class OrderAdminSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    order_detail = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'checked_out', 'total_amount', 'total_price', 'status', 'owner', 'order_detail']
