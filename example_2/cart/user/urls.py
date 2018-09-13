from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', UserOrderDetailView.as_view()),
    url(r'^(?P<pk>[0-9]+)$', OrderDetailView.as_view()),
    url(r'^list/?$', OrderListDetailView.as_view()),
    url(r'^product/(?P<pk>[0-9]+)$', OrderProductView.as_view()),
    url(r'^submit/?$', SubmitOrderView.as_view()),
    url(r'^test/?$', Test.as_view())
]
