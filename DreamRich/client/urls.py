from django.conf.urls import url
from client.views import ExampleView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^auth/', ExampleView.as_view()),
]+router.urls
