from django.db import models
from ..core.models import Agent
from ..core.models import Shop
from django.shortcuts import reverse

RESULT_VISIT_CHOICES = (
    ('visit', 'Посетил'),
    ('invoice', 'Заявка'),
    ('canceled', 'Отменено'),
)


class Visit(models.Model):
    _visitTime = None
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, verbose_name='Агент', help_text='Агент')
    visitDate = models.DateTimeField(verbose_name='Дата/время посещения',
                                     help_text='Дата/время посещения торговой точки')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Торговая точка', help_text='Торговая точка')
    note = models.CharField(max_length=200, verbose_name='Примечание к посещению', help_text='Примечание к посещению')
    result = models.CharField(max_length=20, choices=RESULT_VISIT_CHOICES, verbose_name='Результат посещения',
                              help_text='Результат посещения')
    marked = models.BooleanField(verbose_name='Пометка удаления', help_text='Пометка удаления')

    def __str__(self):
        return f"Посещение {self.id} от {self.visitDate}; агент: {self.agent}"

    def get_absolute_url(self):
        return reverse('visit_url', kwargs={'id': self.id})

    @property
    def visitTime(self):
        return self._visitTime

    @visitTime.setter
    def visitTime(self, value):
        self._visitTime = value

    def get_invoices(self):
        return self.invoice_set.all()
