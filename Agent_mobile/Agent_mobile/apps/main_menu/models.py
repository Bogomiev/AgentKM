from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Имя агента')

    def __str__(self):
        return self.name

    def available_shops(self):
        available_shops = AgentShop.objects.filter(agent=self).values_list('shop_id')
        return Shop.objects.filter(id__in=available_shops).order_by('name')

    def available_shops_with_filter(self, filter='...'):
        available_shops_id = AgentShop.objects.filter(agent=self).values_list('shop_id')

        if filter != '...':
            clients = Client.objects.filter(name__istartswith=filter)
            shops = Shop.objects.filter(client__in=clients, id__in=available_shops_id).order_by('name')
        else:
            shops = Shop.objects.filter(id__in=available_shops_id).order_by('name')

        shop_list = [{'value': 0, 'name': '---------'}]

        for shop in shops:
            shop_list.append({'value': shop.id, 'name': shop.__str__()})

        return shop_list

    @staticmethod
    def get_Agent(request):
        user = auth.get_user(request)
        agent = {'user': user,
                 'id': 0,
                 'name': '',
                 'ref': None}

        if user.is_authenticated:
            try:
                _agent = Agent.objects.get(user_id=user.id)
                agent['user'] = _agent.user
                agent['id'] = _agent.id
                agent['name'] = _agent.name
                agent['ref'] = _agent
            except Agent.DoesNotExist:
                pass
        return agent


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование клиента', db_index=True)
    fullName = models.CharField(max_length=250, verbose_name='Полное наименование')
    inn = models.CharField(max_length=12, verbose_name='ИНН клиента', db_index=True)
    kpp = models.CharField(max_length=9, verbose_name='КПП клиента')
    okpo = models.CharField(max_length=10, verbose_name='ОКПО клиента')
    adress = models.CharField(max_length=250, verbose_name='Адрес клиента')
    phon = models.CharField(max_length=100, verbose_name='Телефон клиента')
    marked = models.BooleanField(verbose_name='Пометка удаления', help_text='Пометка удаления')

    def __str__(self):
        return self.name


class Shop(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', db_index=True)
    name = models.CharField(max_length=200, verbose_name='Адрес торговой точки')
    kpp = models.CharField(max_length=9, verbose_name='КПП точки')
    phon = models.CharField(max_length=100, verbose_name='Телефон торговой точки')
    marked = models.BooleanField(verbose_name='Пометка удаления')

    def __str__(self):
        return f'{self.client.__str__()}: {self.name}'


class AgentShop(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, verbose_name='Агент', db_index=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Торговая точка', db_index=True)

    def __str__(self):
        return f'{self.agent.__str__()} - {self.shop.name}'
