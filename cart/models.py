from django.db import models
from authentication.models import User 
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes import fields
from payments.models import Transactions

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    is_paid = models.BooleanField(default=False)
    uid = models.UUIDField(default=uuid.uuid4)
    session_id = models.CharField(max_length=100,blank=True,null=True)
    transactions = GenericRelation(Transactions)
    
    #for the total number of food and soup quantites in the cart
    def total_quantity(self):
        cartitems = self.cartitems.all()
        total_price = sum([item.quantity for item in cartitems])
        return total_price

    #for the total amount of food and soup prices in the cart
    def total_price(self): 
        cartitems = self.cartitems.all() 
        total_price = sum(item.total_price(item.food_category) for item in cartitems)
        return total_price  
    
    def __str__(self):
            try:
                return self.user.username
            except:
                return self.session_id

    

class CartItemsFood(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    food_category = models.CharField(max_length=30,default="mini box")
    protein = models.CharField(max_length=30,default="beef")
    subprotein = models.CharField(max_length=30,default="fried beef")
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    transactions = GenericRelation(Transactions)
    
    #for each items in cart amount
    def total_price(self,food_category):
        food_model = ContentType.objects.get(model="food")
        soup_model = ContentType.objects.get(model="soup")
        if self.content_type == food_model:
            total_price = self.quantity*self.content_object.food_price 
        elif self.content_type == soup_model and food_category == "mini":
            total_price = self.quantity*self.content_object.mini_box_price
        elif self.content_type == soup_model and food_category == "medium":
            total_price = self.quantity*self.content_object.medium_box_price
        else:
            total_price = self.quantity*self.content_object.mega_box_price
        return total_price
    

    def __str__(self):
        
        return f"{self.content_object} {self.food_category}"
    
    