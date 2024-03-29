from django.shortcuts import render
from food_app.models import Food,Soup
from cart.models import Cart,CartItemsFood
from django.contrib import messages
from django.http.response import JsonResponse
import json
from django.contrib.contenttypes.models import ContentType
import math
import random
import uuid
from . forms import ProteinForm



# Create your views here.

#what food box function does is, first, I used a for loop on the model Food, then listed all the field in the models
#such as: image,food_item,food_price and food slug. put the=m in a list
#and then append them into a list and did the same for all the objects in the model.
food = Food.objects.all().order_by('food_item')
soup = Soup.objects.all().order_by('soup_item')


def food_box(request):
    form = ProteinForm()
    if request.method == "POST":
        form = ProteinForm(request.POST)
        if form.is_valid():
            form.save()
    
    return render(request,'food_app/food_box_kunkky.html',{'food':food,'form':form})


def soup_box(request):
    
    return render(request,'food_app/soup_box_kunkky.html',{'soup':soup})



def add_to_cart(request):

    data = json.loads(request.body)
    product_id = data['id']
    product = food.get(pk=product_id)
    id = product.pk
    num_of_items = ""
    
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user,is_paid=False)
            
        cart_user = Cart.objects.get(user=request.user)
        content = ContentType.objects.get(model="food")
        cartitems, created = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,object_id=id)

        cartitems.quantity += 1
        cartitems.save()
        num_of_items = cart_user.total_quantity()
    
    else:
        try:
            cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
            content = ContentType.objects.get(model="food")
            cartitems, created = CartItemsFood.objects.get_or_create(cart=cart,content_type=content,object_id=id)
            
            cartitems.quantity += 1
            cartitems.save()
            num_of_items = cart.total_quantity()
        except:
            request.session['cart_users'] = str(uuid.uuid4())
            cart = Cart.objects.create(session_id=request.session['cart_users'],is_paid=False)
            cart_user = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
            content = ContentType.objects.get(model="food")
            cartitems, created = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,object_id=id)
            
            cartitems.quantity += 1
            cartitems.save()
            num_of_items = cart_user.total_quantity()
    
    return JsonResponse(num_of_items,safe=False)



def change_protein(request):
    data = json.loads(request.body)
    protein_id = data['protein_id']
    print(protein_id)
    
    return JsonResponse("it is working ooo",safe=False)
