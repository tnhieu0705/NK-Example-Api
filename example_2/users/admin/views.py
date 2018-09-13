import uuid
import stripe
from django.conf import settings

from django.contrib.auth.hashers import make_password
from django.utils import timezone

from example_2.base.constants.common import ValidationMessages
from example_2.base.permissions import IsAdmin
from example_2.payments.models import Vendor
from example_2.users.models import User
from example_2.users.serializers import UserSerializer, UpdateUserSerializer, CreateUserSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ListCreateView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        user = User.objects.filter(deleted_at=None)
        ser = UserSerializer(user, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = CreateUserSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            data = ser.validated_data
            data['username'] = str(uuid.uuid4())
            password = '123456'
            if 'password' in data:
                del data['password']
            if 'password_confirm' in data:
                del data['password_confirm']
            data['password'] = make_password(password)
            ser.save(created_by=request.user.id)
            if data['role_id'] == 4:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                try:
                    account = stripe.Account.create(
                        type='custom',
                        country='US',
                        email=data['email']
                    )
                except Exception as e:
                    raise e
                if account:
                    Vendor.objects.create(stripe_id=account.id, user_id=ser.data['id'])
        return Response(ser.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk, deleted_at=None)
            ser = UserSerializer(user, many=False)
            return Response(ser.data)
        except:
            msg = {'error': True, 'message': 'User is not exist.'}
            return Response(msg)

    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk, deleted_at=None)
            ser = UpdateUserSerializer(user, data=request.data)
            if ser.is_valid(raise_exception=True):
                data = ser.validated_data
                if data.get('password') and (data['password'] != data['password_confirm']):
                    msg = {'error': True, 'message': ValidationMessages.PasswordsDoesNotMatch}
                    return Response(msg)
                if data.get('password'):
                    data['password'] = make_password(data['password'])
                    del data['password_confirm']
            ser.save(modified_by=request.user.id)
            return Response(ser.data)
        except:
            msg = {'error': True, 'message': 'User is not exist.'}
            return Response(msg)

    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk, deleted_at=None)
            if user.role_id == 4:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                account = stripe.Account.retrieve(user.vendor.stripe_id)
                if account:
                    account.delete()
                    vendor = Vendor.objects.get(stripe_id=user.vendor.stripe_id)
                    vendor.delete()
                    user.deleted_at = timezone.now()
                    user.deleted_by = request.user.id
                    user.save()
            else:
                user.deleted_at = timezone.now()
                user.deleted_by = request.user.id
                user.save()
            return Response(dict(message='USER has been deleted.'))
        except:
            msg = {'error': True, 'message': 'User is not exist.'}
            return Response(msg)
