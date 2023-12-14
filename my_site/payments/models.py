from django.db import models
from cart.models import CartItemsFood
from food_app.models import Food,Soup

# Create your models here.

'''
class CartTransactions(models.Model):
    status = models.CharField(max_length=50)
    cart = models.ForeignKey(CartItemsFood,on_delete=models.CASCADE,related_name="cart_in_cart_transactions")
    tx_ref = models.IntegerField()
    
    def __str__(self):
        return f"{self.cart.user}, {self.cart.content_object}"


class FoodTransactions(models.Model):
    status = models.CharField(max_length=50)
    food = models.ForeignKey(Food,on_delete=models.CASCADE,related_name="food_transactions")
    tx_ref = models.IntegerField()
    
    def __str__(self):
        return f"{self.food.food_item}, {self.food.food_price}"
    
    
class ProductTransactions(models.Model):
    status = models.CharField(max_length=50)
    soup = models.ForeignKey(Soup,on_delete=models.CASCADE,related_name="soup_transactions")
    tx_ref = models.IntegerField()
    
    def __str__(self):
        return f"{self.soup.soup_item}"
'''

