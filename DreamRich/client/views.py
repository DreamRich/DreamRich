from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
import json
from rest_framework import viewsets
from client.serializers import (
        AddressSerializer,
        DependentSerializer,
        ActiveClientSerializer,
        BankAccountSerializer
)

class ActiveClientViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveClientSerializer
    queryset = ActiveClient.objects.all()
