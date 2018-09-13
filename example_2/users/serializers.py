from example_2.base.constants.common import AppChoices
from example_2.users.models import User, Login
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, validators=[UniqueValidator(queryset=User.objects.all())])
    role_id = serializers.ChoiceField(AppChoices.RolesForRegister)
    password = serializers.CharField(min_length=6, max_length=65)
    password_confirm = serializers.CharField(min_length=6, max_length=65)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role_id', 'password', 'password_confirm']


class LoginWebSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(min_length=6, max_length=65)

    class Meta:
        model = Login
        fields = ['email', 'password']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role_id', 'image_url']


class ProfileNameUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=65)
    new_password = serializers.CharField(min_length=6, max_length=65)
    new_password_confirm = serializers.CharField(min_length=6, max_length=65)

    class Meta:
        model = User
        fields = ['password', 'new_password', 'new_password_confirm']


# ADMIN ROLE
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role_id', 'is_active', 'image_url']


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, validators=[UniqueValidator(queryset=User.objects.all())])
    role_id = serializers.ChoiceField(AppChoices.RolesForAdminManageUsers)
    password = serializers.CharField(min_length=6, max_length=65, required=False)
    password_confirm = serializers.CharField(min_length=6, max_length=65, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role_id', 'password', 'password_confirm', 'is_active']


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    role_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=6, max_length=65, required=False)
    password_confirm = serializers.CharField(min_length=6, max_length=65, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role_id', 'password', 'password_confirm', 'is_active']
