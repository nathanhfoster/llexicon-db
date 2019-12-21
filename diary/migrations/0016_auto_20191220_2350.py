# Generated by Django 2.1.11 on 2019-12-20 23:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0015_auto_20191219_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='address',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date_created_by_author',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 20, 23, 50, 20, 359708, tzinfo=utc)),
        ),
    ]
