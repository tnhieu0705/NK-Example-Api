from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^token?$', StripeTokenView.as_view()),
    url(r'(?P<pk>[0-9]+)$', PaymentCreateView.as_view())
]
