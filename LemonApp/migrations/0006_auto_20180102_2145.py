# Generated by Django 2.0 on 2018-01-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LemonApp', '0005_pptcomment_ppt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pptlist',
            name='page_count',
            field=models.IntegerField(default=0, null=True, verbose_name='页数'),
        ),
    ]