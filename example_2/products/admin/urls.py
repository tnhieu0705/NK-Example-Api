from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^$', ListCreateProductView.as_view()),
    url(r'^(?P<pk>[0-9]+)$', RetrieveUpdateDestroyProductView.as_view()),
    url(r'^search/(?P<name>.+)$', ProductSearchView.as_view())
]
