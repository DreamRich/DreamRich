from rest_framework import routers
from django.conf.urls import url
from financial_planning.views import (
    RegularCostViewSet,
    CostTypeViewList,
    CostManagerViewSet,
)


app_name = 'financial_planning'

router = routers.DefaultRouter()
router.register(r'^regularcost', RegularCostViewSet)
router.register(r'^costmanager', CostManagerViewSet)


urlpatterns = [url(r'costtype/$', CostTypeViewList.as_view())] + router.urls
