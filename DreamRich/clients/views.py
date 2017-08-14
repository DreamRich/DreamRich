from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
import json

def create(request):
	return render(request, 'clients/create.html', {})

def show(request, client_id):
	client = get_object_or_404(Client, pk=client_id)
	context = {'client': 2}
	return HttpResponse(json.dumps(context))

def list(request):
	clients_list = Client.objects.order_by('-name')
	context = {'clients_list': clients_list}
	return render(request, 'clients/list.html', context)