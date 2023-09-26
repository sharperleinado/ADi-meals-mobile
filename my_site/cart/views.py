from django.shortcuts import render
from food_app.models import Food,Soup
from django.contrib import messages
from django.shortcuts import redirect
from .models import CartItemsFood,Cart
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.http.response import JsonResponse,HttpResponse
import json

# Create your views here.



def cart_items(request):
    food_list = []
    food_model = ContentType.objects.get(model="food")
    soup_model = ContentType.objects.get(model="soup")
    
    cart_items = CartItemsFood.objects.all()
    for item in cart_items:
        if item.content_type == food_model:
            id = item.object_id
            content_type = item.content_type
            food = Food.objects.get(pk=id)
            quantity = item.quantity
            food_category = item.food_category
            total_food_price = item.total_price()
            item_list = [food,content_type,id,quantity,food_category,total_food_price]
            food_list.append(item_list)
        else:
            id2 = item.object_id
            content_type_2 = item.content_type
            soup = Soup.objects.get(pk=id2)
            quantity2 = item.quantity
            soup_category = item.food_category
            soup_price = item.soup_price()
            total_soup_price = item.total_price()
            item_list = [soup,content_type_2,id2,quantity2,soup_category,soup_price,total_soup_price]
            food_list.append(item_list)
            
        total_quantities = item.all_food_and_soup_quantities()
        total_price = item.all_soup_and_food_prices()
    
    return render(request,'cart/cart-items.html',{'items':food_list,'food_model':food_model,'soup_model':soup_model,
                                                  'total_quantities':total_quantities,'total_price':total_price})

