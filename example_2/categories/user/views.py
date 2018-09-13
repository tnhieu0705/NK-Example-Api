from example_2.categories.models import Category
from example_2.categories.serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class ListCategoriesView(APIView):
    permission_classes = []

    def get(self, request):
        categories = Category.objects.all()
        ser = CategorySerializer(categories, many=True)
        return Response(ser.data)


class RetrieveCategoryView(APIView):
    permission_classes = []

    def get(self, request, pk):
        try:
            category = Category.objects.filter(id=pk, deleted_at=None).first()
            ser = CategorySerializer(category, many=False)
            return Response(ser.data)
        except:
            return Response(dict(message='This CATEGORY is not exist.'))


class SearchCategoryView(APIView):
    permission_classes = []

    def get(self, request, name):
        categories = Category.objects.filter(name__icontains=name, deleted_at=None)
        if categories.count() > 0:
            ser = CategorySerializer(categories, many=True)
            return Response(ser.data)
        return Response(dict(message='Not found.'))
