from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^client/', include('client.urls')),
    url(r'^api/', include([
        url(r'^client/', include('client.api_urls')),
        url(r'^dreamrich/', include('DreamRich.api_urls')),
        url(r'^patrimony/', include('patrimony.api_urls'))     
    ]))
]
