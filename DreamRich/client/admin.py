from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Dependent)
admin.site.register(Address)
admin.site.register(BankAccount)
