# Generated by Django 3.0.3 on 2020-03-04 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='okpo',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='ОКПО клиента'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phon',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Телефон клиента'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='phon',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Телефон торговой точки'),
        ),
    ]
