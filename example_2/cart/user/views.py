import json

from example_2.base.services.cart import CartManager
from example_2.cart.models import Order
from example_2.cart.serializers import OrderSerializer, OrderAdminSerializer
from example_2.products.models import Product
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from rest_framework.response import Response
from rest_framework.views import APIView


class UserOrderDetailView(APIView):

    def get(self, request):
        user = request.user
        try:
            order = Order.objects.get(owner=user.id, checked_out=False)
            ser = OrderSerializer(order, many=False)
            return Response(ser.data)
        except:
            return Response(dict(message='None.'))


class OrderListDetailView(APIView):

    def get(self, request):
        user = request.user
        if not user.is_anonymous:
            try:
                order = Order.objects.filter(owner=user.id, checked_out=True)
                ser = OrderSerializer(order, many=True)
                return Response(ser.data)
            except:
                return Response(dict(message='None.'))


class OrderDetailView(APIView):

    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk, checked_out=True)
            ser = OrderAdminSerializer(order, many=False)
            return Response(ser.data)
        except Exception as e:
            raise e


class OrderProductView(APIView):

    def post(self, request, pk):
        user = request.user
        if user.is_anonymous:
            cart = CartManager(request)
        else:
            cart = CartManager(request, user)
        try:
            product = Product.objects.get(id=pk, deleted_at=None)
            cart.add(product, product.price, 1)
            return Response(dict(message='SUCCESS'))
        except:
            msg = {'error': True, 'message': 'This PRODUCT is not exist.'}
            return Response(msg)

    def put(self, request, pk):
        user = request.user
        json_params = json.loads(request.body)
        quantity = int(json_params['quantity'])
        if user.is_anonymous:
            cart = CartManager(request)
        else:
            cart = CartManager(request, user)
        try:
            product = Product.objects.get(id=pk, deleted_at=None)
            cart.update(product, product.price, quantity)
            return Response(dict(message='SUCCESS'))
        except Exception as e:
            raise e

    def delete(self, request, pk):
        user = request.user
        if user.is_anonymous:
            cart = CartManager(request)
        else:
            cart = CartManager(request, user)
        if cart.count() > 0:
            try:
                product = Product.objects.get(id=pk, deleted_at=None)
                cart.remove(product)
                return Response(dict(message='PRODUCT has been removed.'))
            except:
                msg = {'error': True, 'message': 'This PRODUCT is not exist.'}
                return Response(msg)
        else:
            return Response(dict(message='CART is empty.'))


class SubmitOrderView(APIView):

    def post(self, request):
        user = request.user
        if not user.is_anonymous:
            try:
                order = Order.objects.get(owner=user, checked_out=False)
                if order.order_detail.count() > 0:
                    order.checked_out = True
                    order.save()

                    pnconfig = PNConfiguration()
                    pnconfig.publish_key = "pub-c-fdd957cd-be31-427f-9e91-9c2bed852ba9"
                    pnconfig.subscribe_key = "sub-c-c7c2aa20-b56f-11e8-b6ef-c2e67adadb66"
                    pnconfig.ssl = True

                    pubnub = PubNub(pnconfig)

                    my_listener = SubscribeListener()
                    pubnub.add_listener(my_listener)

                    # pubnub.subscribe().channels('my_channel').execute()
                    # my_listener.wait_for_connect()
                    # print('connected')

                    pubnub.publish().channel('my_channel').message({
                        'message': 'Order success.',
                        'order': order.id,
                        'owner': user.id
                    }).sync()

                    # info = my_listener.wait_for_message_on('my_channel')
                    # print(info.message)

                    # pubnub.unsubscribe().channels('my_channel').execute()
                    # my_listener.wait_for_disconnect()
                    # print('unsubscribe')

                    pubnub.history().channel('my_channel').count(100).sync()

                    return Response(dict(message='DONE.'))
                else:
                    return Response(dict(message='CART is empty.'))
            except:
                msg = {'error': True, 'message': 'This CART is not exist.'}
                return Response(msg)


class Test(APIView):

    def get(self, request):
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = "sub-c-c7c2aa20-b56f-11e8-b6ef-c2e67adadb66"
        pnconfig.publish_key = "pub-c-fdd957cd-be31-427f-9e91-9c2bed852ba9"
        pnconfig.ssl = True

        pubnub = PubNub(pnconfig)

        my_listener = SubscribeListener()
        pubnub.add_listener(my_listener)

        pubnub.subscribe().channels("test_channel").execute()
        my_listener.wait_for_connect()
        print('connected')

        pubnub.publish().channel('test_channel').message({
            'order': 16,
            'owner': 1
        }).sync()
        info = my_listener.wait_for_message_on('test_channel')
        print(info.message)
        print(pubnub.time())
        print(pubnub.timestamp())

        pubnub.unsubscribe().channels('test_channel').execute()
        my_listener.wait_for_disconnect()
        print('unsubscribe')

        envelope = pubnub.history().channel('test_channel').count(100).sync()
        print(envelope)

        return Response(dict(info.message))
