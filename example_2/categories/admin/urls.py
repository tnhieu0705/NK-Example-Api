from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', ListCreateCategoryView.as_view()),
    url(r'^(?P<pk>[0-9]+)$', RetrieveUpdateDestroyCategoryView.as_view()),
    url(r'^search/(?P<name>.+)$', CategorySearchView.as_view())
]