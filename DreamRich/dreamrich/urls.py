from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include([
        url(r'^client/', include('client.urls')),
        url(r'^patrimony/', include('patrimony.urls')),
        url(r'^employee/', include('employee.urls')),
    ]))
]
