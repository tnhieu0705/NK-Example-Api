import uuid

from django.utils import timezone

from example_2.base.permissions import IsAdmin
from example_2.categories.models import Category
from example_2.categories.serializers import CategorySerializer, CreateCategorySerializer, UpdateCategorySerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ListCreateCategoryView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        categories = Category.objects.filter(deleted_at=None)
        ser = CategorySerializer(categories, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = CreateCategorySerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            data = ser.validated_data
            if not data.get('code') or data.get('code') == '':
                code = str(uuid.uuid4())
                data['code'] = code
            else:
                data['code'] = data['code']
            ser.save(created_at=request.user.id)
        return Response(ser.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyCategoryView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        try:
            category = Category.objects.get(id=pk, deleted_at=None)
            ser = CategorySerializer(category, many=False)
            return Response(ser.data)
        except:
            msg = {'error': True, 'message': 'This CATEGORY does not exist.'}
            return Response(msg)

    def put(self, request, pk):
        try:
            category = Category.objects.get(id=pk, deleted_at=None)
            ser = UpdateCategorySerializer(category, data=request.data)
            if ser.is_valid(raise_exception=True):
                ser.save(modified_by=request.user.id)
            return Response(ser.data)
        except:
            msg = {'error': True, 'message': 'This CATEGORY does not exist.'}
            return Response(msg)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(id=pk, deleted_at=None)
            category.deleted_at = timezone.now()
            category.deleted_by = request.user.id
            category.is_active = False
            category.save()
            return Response(dict(message='CATEGORY is deleted.'))
        except:
            msg = {'error': True, 'message': 'This CATEGORY does not exist.'}
            return Response(msg)


class CategorySearchView(APIView):
    permission_classes = []

    def get(self, request, name):
        categories = Category.objects.filter(name__icontains=name, deleted_at=None)
        if categories.count() > 0:
            ser = CategorySerializer(categories, many=True)
            return Response(ser.data)
        return Response(dict(message='Not found.'))
