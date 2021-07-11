from django.db import models
from django.utils import timezone
from ..core.models import Agent
from ..core.models import Client
from ..core.models import Shop
from ..core.models import Product
from ..visits.models import Visit
from django.db import models

STATUS_CHOICES = (
    (0, 'Новая'),
    (1, 'Создана'),
    (2, 'Отправлена'),
    (3, 'Отменена'),
)


class PriceType(models.Model):
    guid = models.CharField(max_length=32, unique=True, verbose_name='Уникальный идентификатор', db_index=True)
    marked = models.BooleanField(verbose_name='Пометка удаления')
    name = models.CharField(verbose_name='Наименование типа цены', max_length=50)


class Price(models.Model):
    price_type = models.ForeignKey(PriceType, on_delete=models.PROTECT, verbose_name='Тип цены')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Тип цены')
    price = models.DecimalField(verbose_name='Цена товара', max_digits=15, decimal_places=2, default=0)


class Promo(models.Model):
    guid = models.CharField(max_length=32, unique=True, verbose_name='Уникальный идентификатор', db_index=True)
    marked = models.BooleanField(verbose_name='Пометка удаления')
    name = models.CharField(verbose_name='Наименование промоакции', max_length=50)


class Invoice(models.Model):
    guid = models.CharField(max_length=32, unique=True, verbose_name='Уникальный идентификатор', db_index=True)
    visit = models.ForeignKey(Visit, on_delete=models.PROTECT, verbose_name='Визит', db_index=True)
    date = models.DateTimeField(max_length=200, verbose_name='Дата', db_index=True)
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, verbose_name='Агент', db_index=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Клиент')
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT, verbose_name='Торговая точка')
    price_type = models.ForeignKey(PriceType, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Тип цены')
    promo = models.ForeignKey(Promo, on_delete=models.PROTECT, verbose_name='Акция', blank=True, null=True)
    marked = models.BooleanField(verbose_name='Пометка удаления')
    total_summ = models.DecimalField(verbose_name='Сумма документа', max_digits=15, decimal_places=2, default=0)
    to_accounting = models.BooleanField(verbose_name='БУ', default=False)
    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=STATUS_CHOICES,  default=0, db_index=True)

    def __str__(self):
        return f'Заявка от {timezone.localtime(self.date).strftime("%d.%m.%y")} на {self.total_summ}.руб;' \
               f' {self.client.__str__()} '


class InvoiceItem(models.Model):
    ref = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name='Ссылка', db_index=True)
    num = models.IntegerField(verbose_name='Номер строки')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    number = models.DecimalField(verbose_name='Количество товара', max_digits=15, decimal_places=3, default=0)
    price = models.DecimalField(verbose_name='Цена товара', max_digits=15, decimal_places=2, default=0)
    summ = models.DecimalField(verbose_name='Сумма товара', max_digits=15, decimal_places=2, default=0)
    discont = models.DecimalField(verbose_name='Скидка', max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.product.__str__()} - {self.number}'
