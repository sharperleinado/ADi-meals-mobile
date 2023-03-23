from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from food_app.models import Food,Soup
from .models import Cart
from django.contrib import messages
from django.shortcuts import redirect
from .models import CartItemsFood

# Create your views here.


def cart_items(request): 

    items_in_cart = CartItemsFood.objects.all()
    length = len(items_in_cart)
        
    return render(request,'cart/cart-items.html',{'items':items_in_cart,'len':length})

