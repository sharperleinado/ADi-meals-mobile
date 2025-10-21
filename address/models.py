from django.db import models
from authentication.models import User

# Create your models here.


class UserAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    state = models.CharField(max_length=50)
    division = models.CharField(max_length=50, null=True)
    lga = models.CharField(max_length=50, null=True)
    lcda = models.CharField(max_length=50, null=True)
    street_name = models.CharField(max_length=300, null=True)

    def __str__(self):
        return f"{self.lga}, {self.lcda}, {self.street_name}."
    
    
