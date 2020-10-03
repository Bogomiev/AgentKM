# Generated by Django 3.0.3 on 2020-03-04 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='Уникальный идентификатор')),
                ('name', models.CharField(max_length=100, verbose_name='Имя агента')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='Уникальный идентификатор')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Наименование клиента')),
                ('fullName', models.CharField(max_length=250, verbose_name='Полное наименование')),
                ('inn', models.CharField(db_index=True, max_length=12, verbose_name='ИНН клиента')),
                ('kpp', models.CharField(max_length=9, verbose_name='КПП клиента')),
                ('okpo', models.CharField(max_length=10, verbose_name='ОКПО клиента')),
                ('adress', models.CharField(max_length=250, verbose_name='Адрес клиента')),
                ('phon', models.CharField(max_length=100, verbose_name='Телефон клиента')),
                ('marked', models.BooleanField(verbose_name='Пометка удаления')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='Уникальный идентификатор')),
                ('name', models.CharField(max_length=200, verbose_name='Адрес торговой точки')),
                ('kpp', models.CharField(max_length=9, verbose_name='КПП точки')),
                ('phon', models.CharField(max_length=100, verbose_name='Телефон торговой точки')),
                ('marked', models.BooleanField(verbose_name='Пометка удаления')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Client', verbose_name='Клиент')),
            ],
        ),
        migrations.CreateModel(
            name='AgentShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Agent', verbose_name='Агент')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Shop', verbose_name='Торговая точка')),
            ],
        ),
    ]
