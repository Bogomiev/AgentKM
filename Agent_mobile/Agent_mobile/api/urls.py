from django.conf.urls import url
from .agent_api import AgentAPI
from .client_api import ClientAPI
from .shop_api import ShopAPI

urlpatterns = [
    url(r'^agent$', AgentAPI.as_view()),
    url(r'^agent/(?P<guid>.+)$', AgentAPI.as_view()),
    url(r'^client$', ClientAPI.as_view()),
    url(r'^client/(?P<guid>.+)$', ClientAPI.as_view()),
    url(r'^shop$', ShopAPI.as_view()),
    url(r'^shop/(?P<guid>.+)$', ShopAPI.as_view()),
]