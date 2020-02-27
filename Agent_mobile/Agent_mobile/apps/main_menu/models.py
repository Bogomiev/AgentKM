from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', help_text='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Имя агента', help_text='Имя агента')

    def __str__(self):
        return self.name

    @staticmethod
    def get_Agent(request):
        user = auth.get_user(request)
        agent = {'user': user,
                 'id': 0,
                 'name': ''}

        if user.is_authenticated:
            try:
                _agent = Agent.objects.get(user_id=user.id)
                agent['user'] = _agent.user
                agent['id'] = _agent.id
                agent['name'] = _agent.name
            except Agent.DoesNotExist:
                pass
        return agent


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование клиента', help_text='Наименование клиента')
    fullName = models.CharField(max_length=250, verbose_name='Полное наименование', help_text='Полное наименование')
    inn = models.CharField(max_length=12, verbose_name='ИНН клиента', help_text='ИНН клиента')
    kpp = models.CharField(max_length=9, verbose_name='КПП клиента', help_text='КПП клиента')
    okpo = models.CharField(max_length=10, verbose_name='ОКПО клиента', help_text='ОКПО клиента')
    adress = models.CharField(max_length=250, verbose_name='Адрес клиента', help_text='Адрес клиента')
    phon = models.CharField(max_length=100, verbose_name='Телефон клиента', help_text='Телефон клиента')
    marked = models.BooleanField(verbose_name='Пометка удаления', help_text='Пометка удаления')

    def __str__(self):
        return self.name


class Shop(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', help_text='Клиент')
    name = models.CharField(max_length=200, verbose_name='Адрес торговой точки', help_text='Адрес торговой точки')
    kpp = models.CharField(max_length=9, verbose_name='КПП точки', help_text='КПП точки')
    phon = models.CharField(max_length=100, verbose_name='Телефон торговой точки', help_text='Телефон торговой точки')
    marked = models.BooleanField(verbose_name='Пометка удаления', help_text='Пометка удаления')

    def __str__(self):
        return self.name