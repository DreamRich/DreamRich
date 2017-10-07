from django.conf.urls import url
from dr_auth.views import AuthView
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token
)

urlpatterns = [
    url(r'^$', obtain_jwt_token),
    url(r'^refresh/$', refresh_jwt_token),
    url(r'^password/$', AuthView.as_view()),
]
