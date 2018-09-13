from django.db import models
from django.utils import timezone
from example_2.cart.models import Order, OrderDetail

CART_ID = 'CART_ID'


class CartManager:

    def __init__(self, request, user=None):
        cart_id = request.session.get(CART_ID)
        if user:
            cart = self.create_with_user(request, user)
        elif cart_id:
            cart = self.create_without_user(request, cart_id)
        else:
            cart = self.new(request)
        self.cart = cart

    def create_without_user(self, request, cart):
        try:
            cart = Order.objects.get(id=cart, checked_out=False)
        except Order.DoesNotExist:
            cart = self.new(request)
        return cart

    def create_with_user(self, request, user):
        try:
            cart = Order.objects.get(owner=user, checked_out=False)
        except Order.DoesNotExist:
            cart = self.new(request, user)
        return cart

    # Make new CART
    def new(self, request, user=None):
        cart = Order(created_at=timezone.now(), owner=user)
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    # Add PRODUCT to CART
    def add(self, product, unit_price, quantity=1):
        try:
            item = OrderDetail.objects.get(order=self.cart, product=product)
        except OrderDetail.DoesNotExist:
            item = OrderDetail()
            item.order = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.total_price = unit_price * quantity
            item.save()
        else:
            item.unit_price = unit_price
            item.quantity += int(quantity)
            item.total_price += unit_price * quantity
            item.save()
        self.cart_update()

    # Update PRODUCT
    def update(self, product, unit_price, quantity):
        try:
            item = OrderDetail.objects.get(order=self.cart, product=product)
        except OrderDetail.DoesNotExist:
            pass
        else:
            if quantity == 0:
                item.delete()
            else:
                item.unit_price = unit_price
                item.quantity = quantity
                item.total_price = unit_price * quantity
                item.save()
        self.cart_update()

    # Remove PRODUCT
    def remove(self, product):
        try:
            item = OrderDetail.objects.get(order=self.cart, product=product)
        except OrderDetail.DoesNotExist:
            pass
        else:
            item.delete()
        self.cart_update()

    # ORDER total_amount
    def count(self):
        result = 0
        for item in self.cart.order_detail.all():
            result += 1 * item.quantity
        return result

    # ORDER total_price
    def summary_price(self):
        result = 0
        for item in self.cart.order_detail.all():
            result += item.total_price
        return result

    # Update ORDER(total_amount, total_price)
    def cart_update(self):
        self.cart.total_amount = self.count()
        self.cart.total_price = self.summary_price()
        self.cart.save()
