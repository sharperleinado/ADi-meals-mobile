from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    pass


#class address(models.Model):
#    country = models.CharField(max_length=30)
#    state = models.CharField(max_length=30)
#    city = models.CharField(max_length=50)
#    street_name = models.CharField(max_length=100)