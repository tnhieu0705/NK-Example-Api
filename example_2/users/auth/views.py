import uuid

from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from example_2.base.constants.common import ValidationMessages
from example_2.base.permissions import IsUser
from example_2.users.models import User
from example_2.users.serializers import RegisterSerializer, LoginWebSerializer, ProfileSerializer, \
    ProfileNameUpdateSerializer, ChangePasswordSerializer

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            data = ser.validated_data
            data['username'] = str(uuid.uuid4())
            if data['password'] != data['password_confirm']:
                msg = {
                    'error': True,
                    'message': ValidationMessages.PasswordsDoesNotMatch
                }
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            if 'password_confirm' in data:
                del data['password_confirm']
            data['password'] = make_password(data['password'])
            ser.save()
            msg = {
                'error': False,
                'message': 'Successfully registered.'
            }
            send_mail('Test mail', 'Gz...', 'frankytran1991@gmail.com', ['frankytran1991@gmail.com'], fail_silently=False)
            return Response(msg, status=status.HTTP_201_CREATED)


class LoginWebView(APIView):
    permission_classes = []

    def post(self, request):
        ser = LoginWebSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            token = self.login_web(**ser.validated_data)
            return Response(dict(token=token))

    @staticmethod
    def login_web(email, password):
        user = User.objects.filter(email=email, deleted_at=None).first()
        if not user:
            msg = {
                'error': True,
                'message': 'USER is not exist.'
            }
            return msg
        else:
            if user.check_password(password):
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return token
            else:
                msg = {
                    'error': True,
                    'message': 'Password does not match.'
                }
                return msg


class LogoutView(APIView):
    permission_classes = []

    def get(self, request):
        if hasattr(request, 'session'):
            logout(request)
        return Response(dict(message='Logout.'))

    def post(self, request):
        if hasattr(request, 'session'):
            logout(request)
        return Response(dict(message='Logout.'))


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        ser = ProfileSerializer(user, many=False)
        return Response(ser.data)

    def put(self, request):
        user = request.user
        profile_name_serializer = ProfileNameUpdateSerializer(user, data=request.data)
        if profile_name_serializer.is_valid(raise_exception=True):
            profile_name_serializer.save()
        return Response(dict(message='Profile name updated.'))


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        change_password_serializer = ChangePasswordSerializer(request.user, data=request.data)
        if change_password_serializer.is_valid(raise_exception=True):
            data = change_password_serializer.validated_data
            if not request.user.check_password(data['password']):
                return Response(dict(message='Password is not correct.'))
            if data['new_password'] != data['new_password_confirm']:
                return Response(dict(message=ValidationMessages.PasswordsDoesNotMatch))

            request.user.set_password(data['new_password'])
            request.user.save()
        return Response(dict(message='Password has changed.'))
