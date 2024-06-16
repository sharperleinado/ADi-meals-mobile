from django.shortcuts import render,redirect
from django.urls import reverse 
from food_app.models import Food,Soup
from django.contrib import messages
from .models import CartItemsFood,Cart
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.http.response import JsonResponse,HttpResponse
import json
from authentication.models import Mobile
from payments.views import tx_ref
from food_app.views import food,soup
from django.contrib.sites.shortcuts import get_current_site
from address.models import UserAddress
from django.template import *

# Create your views here.


food_model = ContentType.objects.get(model="food")
soup_model = ContentType.objects.get(model="soup")

def returns_item(items,food_category):
        new_items = []
        for item in items:
            if item.content_type == food_model:
                total_price = item.total_price(item.food_category)
                new_list = [item,total_price]
                new_items.append(new_list)
            elif item.content_type == soup_model and item.food_category == item.food_category:
                total_price = item.total_price(item.food_category)
                new_list = [item,total_price]
                new_items.append(new_list)
        return new_items

def cart_items(request):
    new_cartitems = ""
    cart = ""
    cart_quantity = ""
    username = ""
    email = ""
    mobile = ""
    phone_no = ""
    try:
        username = request.user.username
        email = request.user.email
        mobile = Mobile.objects.get(user=request.user)
        phone_no = mobile.phone_no
    except:
        pass

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_quantity = cart.total_quantity()
            cartitems = cart.cartitems.all()
            new_cartitems = returns_item(cartitems,"mini_box")
        else:
            try:
                cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                cart_quantity = cart.total_quantity()
                cartitems = cart.cartitems.all()
                new_cartitems = returns_item(cartitems,"mini_box")
            except:
                messages.info(request,"Add items to cart to view items!")
                return redirect('cart:cart_items')
    
    except Cart.DoesNotExist:
        messages.error(request,"Add items to cart to view items!")
        pass
        return redirect('cart:cart_items')
    
    return render(request,'cart/cartitems_kunkky.html',{
        'food':food_model,
        'soup':soup_model,
        'new':new_cartitems,
        'username':username,
        'email':email,
        'phone_no': phone_no,
        'tx_ref':tx_ref(),
        })



def cart_buttons(request):
    try:
        new_item = ""
        list_item = ""
        check_carts = ""
        data = json.loads(request.body)
        object_id = data['id']
        name = data['btn_name']
        form = data['form']
        
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItemsFood.objects.filter(cart=cart)
            total_quantities = cart.total_quantity()
            
            if name == "add-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity += 1
                item.save()
                total_quantities = total_quantities + 1
            elif name == "subtract-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity -= 1
                item.save()
                if item.quantity < 1:
                    item.delete()
                total_quantities = total_quantities - 1
            else:
                item = cart_items.get(object_id=object_id,food_category=form)
                item.delete()
                total_quantities = total_quantities - item.quantity
            cartitem_price = item.total_price(item.food_category)
            new_quantity = item.quantity
            total_quantities = total_quantities
            list_item = [cartitem_price,new_quantity,total_quantities]

            
        else:
            cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
            cart_items = CartItemsFood.objects.filter(cart=cart)
            total_quantities = cart.total_quantity() 
            
            if name == "add-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity += 1
                item.save()
                total_quantities = total_quantities + 1
            elif name == "subtract-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity -= 1
                item.save()
                if item.quantity < 1:
                    item.delete()
                total_quantities = total_quantities - 1
            else:
                item = cart_items.get(object_id=object_id,food_category=form)
                item.delete()
                total_quantities = total_quantities - item.quantity
            cartitem_price = item.total_price(item.food_category)
            new_quantity = item.quantity
            total_quantities = total_quantities
            list_item = [cartitem_price,new_quantity,total_quantities]
    except:
        pass

    return JsonResponse(list_item, safe=False)


def clear_all(request):
    data = json.loads(request.body)
    cart = data['okay_value']
    print(cart)

    if request.user.is_authenticated:
        cart_object = Cart.objects.get(user=cart)
        cart_object.delete()
    else:
        cart_object = Cart.objects.get(session_id=cart)
        cart_object.delete()
    
    return JsonResponse(data,safe=False)


def checkout(request):
    address = ""
    cart = ""

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_quantity = cart.total_quantity()
            cartitems = cart.cartitems.all()
            new_cartitems = returns_item(cartitems,"mini_box")
            address = UserAddress.objects.get(user=request.user)
            cartitems = CartItemsFood.objects.filter(cart=cart)
        else:
            try:
                cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                cart_quantity = cart.total_quantity()
                cartitems = cart.cartitems.all()
                new_cartitems = returns_item(cartitems,"mini_box")
            except:
                pass
    except:
        pass

    return render(request,'cart/checkout.html',{
        'address':address,
        'food':food_model,
        'soup':soup_model,
        'new':new_cartitems,
        })

