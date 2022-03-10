# Generated by Django 4.0.2 on 2022-03-10 03:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('country_code', models.CharField(default='+1', max_length=5)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('user_password', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('attempts_left', models.IntegerField(default=10)),
                ('lock', models.DateTimeField(default=datetime.datetime(2022, 3, 9, 23, 5, 35, 36857))),
                ('account_status', models.CharField(default='inactive', max_length=100)),
            ],
        ),
    ]
