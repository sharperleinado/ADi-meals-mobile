from django.shortcuts import render
from food_app.models import Food,Soup
from cart.models import Cart,CartItemsFood
from django.contrib import messages
from django.http.response import JsonResponse
import json
from django.contrib.contenttypes.models import ContentType
import math
import random




# Create your views here.

#what food box function does is, first, I used a for loop on the model Food, then listed all the field in the models
#such as: image,food_item,food_price and food slug. put the=m in a list
#and then append them into a list and did the same for all the objects in the model.
food = Food.objects.all().order_by('food_item')
soup = Soup.objects.all().order_by('soup_item')


def food_box(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItemsFood.objects.filter(cart=cart)
    for item in cart_items:
        total_quantities = item.all_food_and_soup_quantities()
    print(total_quantities)
    
    return render(request,'food_app/food_box.html',{'food':food,'total_quantities':total_quantities})


def soup_box(request):
    
    return render(request,'food_app/soup_box.html',{'soup':soup})



def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data['id']
        product = food.get(pk=product_id) 
        id = product.pk
    
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user,is_paid=False)
            
            cart_user = Cart.objects.get(user=request.user)
            content = ContentType.objects.get_for_model(product)
            cartitems = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,object_id=id)

            cart_object = CartItemsFood.objects.get(cart=cart_user,content_type=content,object_id=id)
            cart_object.quantity += 1
            cart_object.save()
        
            num_of_items = cart_object.all_food_and_soup_quantities()
    except:
        pass

    return JsonResponse(num_of_items,safe=False)


