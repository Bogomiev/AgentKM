from django.contrib import auth
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Agent(models.Model):
    guid = models.CharField(max_length=32, unique=True, verbose_name='Уникальный идентификатор', db_index=True)
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
    guid = models.CharField(max_length=32, unique=True, verbose_name='Уникальный идентификатор', db_index=True)
    name = models.CharField(max_length=100, verbose_name='Наименование клиента', db_index=True)
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    inn = models.CharField(max_length=12, verbose_name='ИНН клиента', db_index=True)
    kpp = models.CharField(max_length=9, verbose_name='КПП клиента', blank=True, null=True)
    okpo = models.CharField(max_length=10, verbose_name='ОКПО клиента', blank=True, null=True)
    adress = models.CharField(max_length=250, verbose_name='Адрес клиента')
    phon = models.CharField(max_length=100, verbose_name='Телефон клиента', blank=True, null=True)
    marked = models.BooleanField(verbose_name='Пометка удаления')

    def __str__(self):
        return self.name


class Shop(models.Model):
    guid = models.CharField(max_length=32, unique=True, verbose_name='Уникальный идентификатор', db_index=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', db_index=True)
    name = models.CharField(max_length=200, verbose_name='Адрес торговой точки')
    kpp = models.CharField(max_length=9, verbose_name='КПП точки', blank=True, null=True)
    phon = models.CharField(max_length=100, verbose_name='Телефон торговой точки', blank=True, null=True)
    marked = models.BooleanField(verbose_name='Пометка удаления')

    def __str__(self):
        return f'{self.client.__str__()}: {self.name}'


class AgentShop(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, verbose_name='Агент', db_index=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Торговая точка', db_index=True)

    def __str__(self):
        return f'{self.agent.__str__()} - {self.shop.name}'


class ProductTree(models.Model):
    guid = models.CharField(max_length=32, unique=True, verbose_name='Уникальный идентификатор', db_index=True)
    code = models.CharField(max_length=11, unique=True, verbose_name='Код товара', db_index=True)
    name = models.CharField(max_length=100, verbose_name='Наименование группы')
    # parent_id = models.IntegerField(verbose_name='id родителя', db_index=True)
    marked = models.BooleanField(verbose_name='Пометка удаления')
    # parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родитель',
                               db_index=True)

    # class MPTTMeta:
    #     order_insertion_by = ['name']

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Product(models.Model):
    guid = models.CharField(max_length=32, unique=True, verbose_name='Уникальный идентификатор', db_index=True)
    code = models.CharField(max_length=11, unique=True, verbose_name='Код товара', db_index=True)
    articul = models.CharField(max_length=11, verbose_name='Артикул')
    name = models.CharField(max_length=100, verbose_name='Наименование товара')
    parent = models.ForeignKey(ProductTree, on_delete=models.CASCADE, verbose_name='Родитель', db_index=True)
    marked = models.BooleanField(verbose_name='Пометка удаления')

    def __str__(self):
        return self.name
