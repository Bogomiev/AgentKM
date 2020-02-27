from django.contrib import admin
from .models import Agent
from .models import Client
from .models import Shop

admin.site.register(Agent)
admin.site.register(Client)
admin.site.register(Shop)
