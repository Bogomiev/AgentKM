from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import routers, serializers, viewsets
from annoying.functions import get_object_or_None
from rest_framework.views import APIView

from .utils import post_api, get_api
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
        _user = get_object_or_None(User, id=agent_json['user'])
        if _user is None:
            raise Exception(f'для агента {agent} указан несуществующий пользователь с id={agent_json["user"]}')
        elif not (agent is None) and agent.user != agent_json['user']:
            raise Exception(f'невозможно привязать агента {agent} к пользователю {_user}: агент привязан к '
                            f' {agent.user}')
        elif agent is None and not(get_object_or_None(Agent, user_id=agent_json['user']) is None):
            raise Exception(f'невозможно создать агента {agent_json["name"]} с пользователем {_user}: к пользователю '
                            f'привязан агент {get_object_or_None(Agent, user_id=agent_json["user"])}')
        else:
            raise Exception(f'невалидные данные: {agent_json}')

    return agent.id


class AgentAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer

    def get(self, request, **kwargs):
        return get_api(request, Agent, AgentSerializer, 'guid', 'Агент', **kwargs)

    def post(self, request, **kwargs):
        return post_api(request, save_agent, 'guid', 'agent', **kwargs)
