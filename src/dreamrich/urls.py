from django.conf.urls import url, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

SCHEMA_VIEW = get_schema_view(
    title='Dream Rich API',
    renderer_classes=[
        OpenAPIRenderer,
        SwaggerUIRenderer])

urlpatterns = [
    url(r'^docs/', SCHEMA_VIEW, name="docs"),
    url(r'^api/', include([
        url(r'^client/', include('client.urls')),
        url(r'^patrimony/', include('patrimony.urls')),
        url(r'^employee/', include('employee.urls')),
        url(r'^auth/', include('dr_auth.urls')),
        url(r'^goal/', include('goal.urls')),
        url(r'^financial_planning/', include('financial_planning.urls')),
    ]))
]
