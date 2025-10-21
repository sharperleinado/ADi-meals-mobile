from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from authentication.models import User


# Create your models here.

food_status_options = {'pending':'preparing',
                        'preparing':'ready',
                        'ready':'out for delivery',
                        'out for delivery':'delivered',
                    }

class Transactions(models.Model):
    order_status = models.CharField(max_length=100,blank=True,choices=[("pending", "pending"),
                                                                       ("preparing", "preparing"),
                                                                       ("ready", "ready"),
                                                                       ("out for delivery", "out for delivery"),
                                                                       ("delivered", "delivered")])
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    cart = models.JSONField(null=True, blank=True)
    boxsize = models.CharField(max_length=30,null=True,blank=True)
    protein = models.CharField(max_length=30,null=True)
    subprotein = models.CharField(max_length=30,null=True)
    status = models.CharField(max_length=50,null=True)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    currency = models.CharField(max_length=20)
    tx_ref = models.IntegerField()
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    delivery = models.DecimalField(max_digits=50, decimal_places=2, default=500)
    cart_item_price = models.JSONField(null=True, blank=True)
    address = models.JSONField(null=True)
    mobile = models.JSONField(null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    datetime = models.DateField(auto_now_add=True,null=True)
    time = models.TimeField(auto_now_add=True,null=True)
        
    def __str__(self):
    
        return f"{self.content_type}, {self.user}, {self.datetime}, {self.time}, {self.object_id}"

