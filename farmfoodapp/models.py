from django.db import models


# Create your models here.
class RegisterModel(models.Model):
    first_name = models.CharField(max_length=50)  # Required Field
    last_name = models.CharField(max_length=50)  # Required Field
    date_of_birth = models.DateTimeField()  # Required Field
    username = models.CharField(max_length=50, default="")  # Optional Field
    email = models.EmailField(max_length=50)  # Required Field
    country_code = models.CharField(max_length=5, default="+1")  # Optional Field
    phone = models.CharField(max_length=15)  # Required Field
    user_password = models.CharField(max_length=50)
