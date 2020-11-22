from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import routers, serializers, viewsets
from annoying.functions import get_object_or_None
from rest_framework.views import APIView
from ..apps.core.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'guid', 'name', 'user']


def save_agent(agent_json):
    agent = get_object_or_None(Agent, guid=agent_json['guid'])
    if agent is None:
        agent_serializer = AgentSerializer(data=agent_json)
    else:
        agent_serializer = AgentSerializer(agent, data=agent_json)

    if agent_serializer.is_valid():
        agent = agent_serializer.save()
    else:
        raise Exception(f'Невалидные данные: {agent_json}')

    return agent.id


class AgentAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer

    def get(self, request, **kwargs):
        if kwargs.__contains__('guid'):
            agent = get_object_or_None(Agent, guid=kwargs['guid'])
            many = False
        else:
            # commit=False
            agent = Agent.objects.all()
            many = True
        try:
            data = AgentSerializer(agent, many=many).data
            response = {'status': 0, 'mess': '', 'data': data}
        except Exception as exc:
            response = {'status': 1, 'mess': f'Агент не определен: {exc}', 'data': {}}

        return JsonResponse(response, safe=False)

    def post(self, request, **kwargs):
        try:
            data = JSONParser().parse(request)['data']
            response_data = {}
            if isinstance(data, list):
                for agent in data:
                    response_data[agent['guid']] = save_agent(agent)
            else:
                response_data[data['guid']] = save_agent(data)
            print(response_data)
            response = {'status': 0, 'mess': '', 'data': response_data}
        except Exception as exc:
            response = {'status': 1, 'mess': f'Ошибка при записи агентов: {exc}', 'data': {}}

        response_status = status.HTTP_201_CREATED if response['status'] == 0 else status.HTTP_400_BAD_REQUEST

        return JsonResponse(response, status=response_status)
