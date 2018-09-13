import json

import stripe
from django.conf import settings
from django.db.models import Sum
from example_2.base.constants.common import AppConstants
from example_2.base.permissions import IsCustomer
from example_2.cart.models import Order, OrderDetail
from example_2.payments.models import Charge, Card, Customer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView


# Create your views here.
class StripeTokenView(APIView):
    permission_classes = []

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        data = json.loads(request.body)
        customer = getattr(self.request.user, 'customer', None)
        print(customer)
        try:
            stripe_token = stripe.Token.create(card=data)
            if customer:
                Card.objects.create(
                    stripe_id=stripe_token.card['id'],
                    customer=customer
                )
                request.session['card_tok'] = stripe_token.id
                return Response(stripe_token)
            else:
                cus = stripe.Customer.create(
                    email=request.user.email,
                    source=stripe_token.id,
                    description="New customer"
                )
                # store local Customer
                Customer.objects.create(stripe_id=cus.id, user=request.user)
                # store local Card
                Card.objects.create(
                    stripe_id=stripe_token.card['id'],
                    customer=customer
                )
                request.session['card_tok'] = stripe_token.id
                return Response(cus)
        except stripe.error.CardError as ce:
            body = ce.json_body
            err = body.get('error', {})
            return Response(err['message'])


class PaymentCreateView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request, pk):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user = request.user
        customer = getattr(self.request.user, 'customer', None)
        if customer:
            try:
                order = Order.objects.filter(id=pk, owner_id=user.id, checked_out=False).first()
                print(11111111)
                od = OrderDetail.objects.values('product__vendor__vendor__stripe_id', 'order_id', 'is_available').annotate(
                    Sum('total_price')).filter(order_id=order.id)
                for item in od:
                    print(22222222)
                    stripe_id = item['product__vendor__vendor__stripe_id']
                    amount = item['total_price__sum']
                    account = stripe.Account.retrieve(stripe_id)
                    if account.payouts_enabled:
                        charge = stripe.Charge.create(
                            amount=amount,
                            currency='usd',
                            source='tok_visa',
                            destination={
                                'account': stripe_id,
                            }
                        )
                    else:
                        print(333333333)
                        order.total_price -= amount
                        order.save()
                        od2 = OrderDetail.objects.filter(product__vendor__vendor__stripe_id=stripe_id, order_id=order.id)
                        for item2 in od2:
                            item2.is_available = False
                            item2.save()
                    if charge.status == 'succeeded':
                        print(44444444)
                        # store local Charge
                        Charge.objects.create(
                            stripe_id=charge.id,
                            customer=customer,
                            amount=charge.amount
                        )
                        order.checked_out = True
                        order.status = AppConstants.RoleOrder.Pending
                        order.save()
                    else:
                        pass
                return Response(dict(message='PAID.'))
            except Exception as e:
                raise e
