from django.db import models
from authentication.models import User 
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

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

    #@property
    #def total_quantity(self):
    #    content = ContentType.objects.get_for_id(self.object_id)
    #    
    #    new_quantity = self.quantity
    #    return new_quantity
    
    def __str__(self):
        return str(self.content_object)
    

#class CartItemsSoup(models.Model):
#    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#    product = models.ForeignKey(Soup, on_delete=models.CASCADE, default=1)
#    quantity = models.IntegerField(default=1)
#    
#    @property
#    def total_quantity(self):
#        new_quantity = self.quantity*self.product.mini_box
#        new_quantity2 = self.quantity*self.product.medium_box
#        new_quantity3 = self.quantity*self.product.mega_box
#        new_quantity_list = [new_quantity,new_quantity2,new_quantity3]
#        return new_quantity_list
#
#    def __str__(self):
#        return self.product.soup_item
    
    