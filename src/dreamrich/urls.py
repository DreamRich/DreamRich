from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    url(r'^docs/', schema_view, name="docs"),
    url(r'^api/', include([
        url(r'^client/', include('client.urls')),
        url(r'^patrimony/', include('patrimony.urls')),
        url(r'^employee/', include('employee.urls')),
        url(r'^auth/', include('dr_auth.urls')),
        url(r'^goal/', include('goal.urls')),
        url(r'^financial_planning/', include('financial_planning.urls')),
    ]))
]
