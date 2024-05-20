# Generated by Django 5.0.4 on 2024-05-20 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planejamento', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='as',
            name='escopo',
            field=models.CharField(max_length=200, verbose_name='Escopo do serviço'),
        ),
        migrations.AlterField(
            model_name='as',
            name='local',
            field=models.CharField(max_length=200, verbose_name='Local do serviço'),
        ),
        migrations.AlterField(
            model_name='rdo',
            name='escopo',
            field=models.CharField(max_length=200, verbose_name='Escopo do serviço'),
        ),
        migrations.AlterField(
            model_name='rdo',
            name='local',
            field=models.CharField(max_length=200, verbose_name='Local do serviço'),
        ),
    ]