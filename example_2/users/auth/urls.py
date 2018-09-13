from django.conf.urls import url
from example_2.users.auth.views import *

urlpatterns = [
    url(r'^register/?$', RegisterView.as_view()),
    url(r'^login/?$', LoginWebView.as_view()),
    url(r'^logout/?$', LogoutView.as_view()),
    url(r'^profile/?$', ProfileView.as_view()),
    url(r'^change-password/?$', ChangePasswordView.as_view())
]
