from django.db import models
from ..main_menu.models import Agent
from ..main_menu.models import Shop

RESULT_VISIT_CHOICES = (
    ('created', 'Создана'),
    ('visit', 'Посетил'),
    ('invoice', 'Заявка'),
    ('canceled', 'Отменено'),
)


class Visit(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, verbose_name='Агент', help_text='Агент')
    visitDate = models.DateTimeField(verbose_name='Дата посещения', help_text='Дата/время посещения торговой точки')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Торговая точка', help_text='Торговая точка')
    note = models.CharField(max_length=200, verbose_name='Примечание к посещению', help_text='Примечание к посещению')
    result = models.CharField(max_length=20, choices=RESULT_VISIT_CHOICES, verbose_name='Результат посещения',
                              help_text='Результат посещения')
    marked = models.BooleanField(verbose_name='Пометка удаления', help_text='Пометка удаления')

    def __str__(self):
        return f"Посещение {self.id} от {self.visitDate}"
