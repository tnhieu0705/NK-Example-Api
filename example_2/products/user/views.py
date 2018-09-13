from example_2.products.models import Product
from example_2.products.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class ListProductView(APIView):
    permission_classes = []

    def get(self, request):
        products = Product.objects.filter(deleted_at=None)
        ser = ProductSerializer(products, many=True)
        return Response(ser.data)


class RetrieveProductView(APIView):
    permission_classes = []

    def get(self, request, pk):
        try:
            product = Product.objects.filter(id=pk, deleted_at=None).first()
            ser = ProductSerializer(product, many=False)
            return Response(ser.data)
        except:
            return Response(dict(message='This PRODUCT is not exist.'))


class SearchProductView(APIView):
    permission_classes = []

    def get(self, request, name):
        products = Product.objects.filter(name__icontains=name, deleted_at=None)
        if products.count() > 0:
            ser = ProductSerializer(products, many=True)
            return Response(ser.data)
        return Response(dict(message='Not found.'))
