# Generated by Django 3.1.7 on 2021-03-22 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20210319_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='brokermodel',
            name='status',
            field=models.CharField(default='OK', editable=False, max_length=20, verbose_name='Статус банкротства'),
        ),
        migrations.AddField(
            model_name='producermodel',
            name='status',
            field=models.CharField(default='OK', editable=False, max_length=20, verbose_name='Статус банкротства'),
        ),
        migrations.AlterField(
            model_name='brokermodel',
            name='city',
            field=models.CharField(choices=[('unassigned', 'Не назначен'), ('IV', 'Айво'), ('WS', 'Вемшир'), ('TT', 'Тортуга'), ('AD', 'Алендор'), ('NF', 'Неверфол'), ('ET', 'Этруа')], max_length=20, verbose_name='Расположение'),
        ),
        migrations.AlterField(
            model_name='producermodel',
            name='city',
            field=models.CharField(choices=[('unassigned', 'Не назначен'), ('IV', 'Айво'), ('WS', 'Вемшир'), ('TT', 'Тортуга'), ('AD', 'Алендор'), ('NF', 'Неверфол'), ('ET', 'Этруа')], max_length=20, verbose_name='Расположение'),
        ),
        migrations.AlterField(
            model_name='sessionmodel',
            name='status',
            field=models.CharField(choices=[('initialized', 'Сессия инициализирована'), ('created', 'Сессия создана'), ('started', 'Сессия заполнена'), ('finished', 'Сессия закончилась')], default='initialized', max_length=15),
        ),
    ]
