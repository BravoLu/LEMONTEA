# Generated by Django 2.0 on 2018-01-01 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LemonApp', '0006_coursecomment_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursecomment',
            old_name='couse_id',
            new_name='course_id',
        ),
    ]
