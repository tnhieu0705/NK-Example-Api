from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'code', 'name', 'description', 'is_active']


class CreateCategorySerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False, max_length=40, allow_blank=True)
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=Category.objects.all())])
    description = serializers.CharField(max_length=150, allow_blank=True, default='')

    class Meta:
        model = Category
        fields = ['id', 'code', 'name', 'description', 'is_active']


class UpdateCategorySerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(max_length=150, allow_blank=True, default='')
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = Category
        fields = ['id', 'code', 'name', 'description', 'is_active']

