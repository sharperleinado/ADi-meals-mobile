from django.db import models
from authentication.models import User 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
    

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    quantity = models.IntegerField(default=1)

    #def __str__(self):
    #    return self.object_id
    
