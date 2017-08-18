from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from client.views import AuthView


urlpatterns = [
    url(r'^auth/$', obtain_jwt_token),
    url(r'^auth/password/', AuthView.as_view())
]
