# Generated by Django 2.1.11 on 2019-11-13 22:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_auto_20191109_0538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date_created_by_author',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 13, 22, 49, 59, 2582, tzinfo=utc)),
        ),
    ]
