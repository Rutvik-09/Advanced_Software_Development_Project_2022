import datetime

from django.db import models


# Create your models here.
class RegisterModel(models.Model):
    first_name = models.CharField(max_length=50)  # Required Field
    last_name = models.CharField(max_length=50)  # Required Field
    date_of_birth = models.DateField()  # Required Field
    email = models.EmailField(max_length=50, unique=True)  # Required Field
    country_code = models.CharField(max_length=5, default="+1")  # Optional Field
    phone = models.CharField(max_length=15, unique=True)  # Required Field
    user_password = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    attempts_left = models.IntegerField(default=10)
    lock = models.DateTimeField(default=datetime.datetime.now())
    account_status = models.CharField(max_length=100, default="inactive")
    is_farmer = models.BooleanField(default=False)
