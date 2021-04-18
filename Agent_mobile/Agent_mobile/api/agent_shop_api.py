from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from annoying.functions import get_object_or_None
from rest_framework.views import APIView
from .utils import get_api, post_api
from ..apps.core.models import AgentShop


class AgentShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentShop
        fields = ['id', 'agent', 'shop']


def save_agent_shop(agent_shop_json):
    agent_shop = get_object_or_None(AgentShop, guid=agent_shop_json['id'])
    if agent_shop is None:
        shop_serializer = AgentShopSerializer(data=agent_shop_json)
    else:
        shop_serializer = AgentShopSerializer(agent_shop, data=agent_shop_json)

    if shop_serializer.is_valid():
        shop = shop_serializer.save()
    else:
        raise Exception(f'невалидные данные: {agent_shop_json}')

    return shop.id


class AgentShopAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AgentShopSerializer

    def get(self, request, **kwargs):
        return get_api(request, AgentShop, AgentShopSerializer, 'id', 'Агент-Магазин', **kwargs)

    def post(self, request, **kwargs):
        return post_api(request, save_agent_shop, 'guid', 'shop', **kwargs)
