from django.conf.urls import url
from rest_framework import routers

from . import views

app_name = 'client'
urlpatterns = [

    # ex: /create/
    url(r'^create?/$', views.create, name='create'),

    # ex: /1/
    url(r'^(?P<client_id>[0-9]+)?/$', views.show, name='show'),

    # ex: /list/
    url(r'^$', views.list, name='list'),

]
