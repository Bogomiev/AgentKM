from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from annoying.functions import get_object_or_None
from rest_framework.views import APIView

from .utils import post_api, get_api
from ..apps.core.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'guid', 'name', 'user']


def create_user(agent_json):
    group_agents = get_object_or_None(Group, name='agents')
    user = User(id=agent_json['user'],
                username=agent_json['name'],
                first_name=agent_json['first_name'],
                last_name=agent_json['last_name'],
                email=agent_json['email'],
                is_active=True)
    user.set_password('+-12345q')
    user.save()
    user.groups.add(group_agents)


def save_agent(agent_json):
    user = get_object_or_None(User, id=agent_json['user'])
    if user is None:
        create_user(agent_json)

    agent = get_object_or_None(Agent, guid=agent_json['guid'])
    if agent is None:
        agent_serializer = AgentSerializer(data=agent_json)
    else:
        agent_serializer = AgentSerializer(agent, data=agent_json)

    if agent_serializer.is_valid():
        agent = agent_serializer.save()
    else:
        user_id = agent_json['user']
        _user = get_object_or_None(User, id=user_id)
        if _user is None:
            raise Exception(f'для агента {agent} указан несуществующий пользователь с id={user_id}')
        elif not (agent is None) and agent.user != user_id:
            raise Exception(f'невозможно привязать агента {agent} к пользователю {_user}: агент привязан к '
                            f' {agent.user}')
        elif agent is None and not (get_object_or_None(Agent, user_id=user_id) is None):
            raise Exception(f'невозможно создать агента {agent_json["name"]} с пользователем {_user}: к пользователю '
                            f'привязан агент {get_object_or_None(Agent, user_id=user_id)}')
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
