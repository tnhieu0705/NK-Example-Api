from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', ListCategoriesView.as_view()),
    url(r'^(?P<pk>[0-9]+)$', RetrieveCategoryView.as_view()),
    url(r'^search/(?P<name>.+)$', SearchCategoryView.as_view())
]
