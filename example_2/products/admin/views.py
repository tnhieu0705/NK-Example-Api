import decimal
import uuid

from django.shortcuts import render
from django.utils import timezone
from example_2.payments.models import Vendor

from example_2.products.models import Category, Product
from example_2.products.serializers import ProductSerializer, CreateProductSerializer, RetrieveUpdateDestroySerializer, VendorSerializer
from example_2.base.permissions import IsAdmin
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class ListCreateProductView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        products = Product.objects.filter(deleted_at=None)
        ser = ProductSerializer(products, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = CreateProductSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            data = ser.validated_data
            if not data.get('code') or data.get('code') == '':
                code = str(uuid.uuid4())
                data['code'] = code
            else:
                data['code'] = data['code']
            if data.get('import_price'):
                a = data['import_price'] * decimal.Decimal(0.3)  # 30%
                data['price'] = data['import_price'] + a
            ser.save(created_at=request.user.id)
        return Response(ser.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyProductView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk, deleted_at=None)
            ser = ProductSerializer(product, many=False)
            return Response(ser.data)
        except:
            msg = {'error': True, 'message': 'This PRODUCT is not exist.'}
            return Response(msg)

    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk, deleted_at=None)
            ser = RetrieveUpdateDestroySerializer(product, data=request.data)
            if ser.is_valid(raise_exception=True):
                data = ser.validated_data
                if data.get('import_price'):
                    a = data['import_price'] * decimal.Decimal(0.3)  # 30%
                    data['price'] = data['import_price'] + a
                ser.save(modified_by=request.user.id)
            return Response(ser.data)
        except:
            msg = {'error': True, 'message': 'This PRODUCT is not exist.'}
            return Response(msg)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk, deleted_at=None)
            product.deleted_at = timezone.now()
            product.deleted_by = request.user.id
            product.is_active = False
            product.save()
            return Response(dict(message='This PRODUCT has been deleted.'))
        except:
            msg = {'error': True, 'message': 'This PRODUCT is not exist.'}
            return Response(msg)


class ProductSearchView(APIView):
    permission_classes = []

    def get(self, request, name):
        products = Product.objects.filter(name__icontains=name, deleted_at=None)
        if products.count() > 0:
            ser = ProductSerializer(products, many=True)
            return Response(ser.data)
        return Response(dict(message='Not found.'))
