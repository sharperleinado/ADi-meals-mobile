from django.db import models
from authentication.models import User 
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
#from food_app.views import food_box_func,soup_box_func

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    #uid = models.UUIDField(default=uuid.uuid4,primary_key=True)

    def __str__(self):
        return self.user.username
    

class CartItemsFood(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return str(self.content_object)
    

