from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from annoying.functions import get_object_or_None
from rest_framework.views import APIView
from .utils import get_api, post_api
from ..apps.core.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'full_name', 'inn', 'kpp', 'okpo', 'address', 'phone', 'marked']


def save_client(client_json):
    client = get_object_or_None(Client, id=client_json['id'])
    if client is None:
        client_serializer = ClientSerializer(data=client_json)
    else:
        client_serializer = ClientSerializer(client, data=client_json)

    if client_serializer.is_valid():
        client = client_serializer.save()
    else:
        raise Exception(f'невалидные данные: {client_json}')

    return client.id


class ClientAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get(self, request, **kwargs):
        return get_api(request, Client, ClientSerializer, 'id', 'Клиент', **kwargs)

    def post(self, request, **kwargs):
        return post_api(request, save_client, 'id', 'client', **kwargs)
