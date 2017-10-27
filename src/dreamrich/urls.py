from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include([
        url(r'^client/', include('client.urls')),
        url(r'^patrimony/', include('patrimony.urls')),
        url(r'^employee/', include('employee.urls')),
        url(r'^auth/', include('dr_auth.urls')),
        url(r'^goal/', include('goal.urls')),
        url(r'^financial_planning/', include('financial_planning.urls')),
    ]))
]
