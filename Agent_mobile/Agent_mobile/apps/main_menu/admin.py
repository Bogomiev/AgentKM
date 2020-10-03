from django.contrib import admin
from ..core.models import Agent
from ..core.models import Client
from ..core.models import Shop
from ..core.models import AgentShop

admin.site.register(Agent)
admin.site.register(Client)
admin.site.register(Shop)
admin.site.register(AgentShop)

