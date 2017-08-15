from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
import json

def create(request):
    return render(request, 'client/create.html', {})

def show(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    context = {'client': 2}
    return HttpResponse(json.dumps(context))

def list(request):
    client_list = Client.objects.order_by('-name')
    context = {'client_list': client_list}

    return render(request, 'client/list.html', context)
