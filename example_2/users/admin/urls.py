from django.conf.urls import url
from example_2.users.admin.views import *

urlpatterns = [
    url(r'^$', ListCreateView.as_view()),
    url(r'^(?P<pk>[0-9]+)/?$', RetrieveUpdateDestroyView.as_view())
]
