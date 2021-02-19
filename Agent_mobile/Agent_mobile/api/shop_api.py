from rest_framework.permissions import IsAuthenticated
from rest_framework import routers, serializers, viewsets
from annoying.functions import get_object_or_None
from rest_framework.views import APIView

from .utils import get_api, post_api
from ..apps.core.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'guid', 'client', 'name', 'kpp', 'phon', 'marked']


def save_shop(shop_json):
    shop = get_object_or_None(Shop, guid=shop_json['guid'])
    if shop is None:
        shop_serializer = ShopSerializer(data=shop_json)
    else:
        shop_serializer = ShopSerializer(shop, data=shop_json)

    if shop_serializer.is_valid():
        shop = shop_serializer.save()
    else:
        raise Exception(f'невалидные данные: {shop_json}')

    return shop.id


class ShopAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    def get(self, request, **kwargs):
        return get_api(request, Shop, ShopSerializer, 'guid', 'Магазин', **kwargs)

    def post(self, request, **kwargs):
        return post_api(request, save_shop, 'guid', 'shop', **kwargs)
