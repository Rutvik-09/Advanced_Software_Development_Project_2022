# Generated by Django 4.0.3 on 2022-03-15 23:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmfoodapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registermodel',
            name='lock',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 15, 20, 49, 10, 998832)),
        ),
    ]
