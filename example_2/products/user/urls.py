from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', ListProductView.as_view()),
    url(r'^(?P<pk>[0-9]+)$', RetrieveProductView.as_view()),
    url(r'^search/(?P<name>.+)$', SearchProductView.as_view())
]
