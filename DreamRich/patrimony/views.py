from rest_framework import viewsets
from patrimony.serializers import (
    PatrimonySerializer,
)
from patrimony.models import (
    Patrimony,
)


class PatrimonyViewSet(viewsets.ModelViewSet):
    serializer_class = PatrimonySerializer
    queryset = Patrimony.objects.all()
