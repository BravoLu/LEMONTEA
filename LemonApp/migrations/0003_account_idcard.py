# Generated by Django 2.0 on 2017-12-31 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LemonApp', '0002_auto_20171231_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='IDcard',
            field=models.CharField(default='-1', max_length=50, verbose_name='学号或教工号'),
        ),
    ]