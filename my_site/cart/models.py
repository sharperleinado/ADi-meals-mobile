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
    uid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.user.username
    

class CartItemsFood(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    food_category = models.CharField(max_length=30,default="mini box")
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    
    
    def soup_price(self):
        if self.food_category == "mini":
            price = 5000
        elif self.food_category == "medium":
            price = 7000
        else:
            price = 10000
        return price
    
    def total_price(self):
        food_model = ContentType.objects.get(model="food")
        food_model_class = food_model.model_class()
        
        soup_model = ContentType.objects.get(model="soup")
        soup_model_class = soup_model.model_class()
        
        if food_model == self.content_type:
            food_price = food_model_class.objects.get(pk=self.object_id)
            price = self.quantity*food_price.food_price
        else:
            price = self.quantity*self.soup_price()
        return price
    
#for the total amount of food and soup prices in the cart
    def all_soup_and_food_prices(self):
        all_prices = []
        cart = Cart.objects.get(user=self.cart.user)
        cart_items = CartItemsFood.objects.filter(cart=cart)
        for item in cart_items:
            all_prices.append(item.total_price())
            total_price = sum(all_prices)
        return total_price
    
#for the total number of food and soup quantites in the cart  
    def all_food_and_soup_quantities(self):
        all_total =[]
        cart = Cart.objects.get(user=self.cart.user)
        cart_items = CartItemsFood.objects.filter(cart=cart)
        for item in cart_items:
            all_total.append(item.quantity)
            total = sum(all_total)
        return total

    def __str__(self):
        return f"{self.content_object} {self.food_category}"
    
    