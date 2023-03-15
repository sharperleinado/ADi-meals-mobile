from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from food_app.models import Food,Soup
from .models import Cart
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.


def cart_add(request,slug):      
        
    return render(request,'cart/cart-items.html',{})


def cart_delete(request,slug):

    return render(request,'cart/cart-items.html',{})
