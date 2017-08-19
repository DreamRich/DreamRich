from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from client.views import AuthView
from client.views import ActiveClientViewSet

app_name = 'client'
urlpatterns = [
    url(r'^auth/$', obtain_jwt_token),
    url(r'^auth/password/', AuthView.as_view())
]

router = routers.DefaultRouter()
router.register(r'', ActiveClientViewSet)

urlpatterns += router.urls
