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
from authentication.models import Mobile
from payments.views import tx_ref
from food_app.views import food,soup

# Create your views here.


def cart_items(request):
    food_model = ContentType.objects.get(model="food")
    try:
        cart = None
        cartitems = []
    
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cartitems = cart.cartitems.all()
            
    except Cart.DoesNotExist:
        messages.info(request,"Add items to cart to view items!")
        return redirect('home')
    
    return render(request,'cart/cartitems.html',{'cart':cart,'items':cartitems,'food':food_model})

'''
def cart_items(request):
    try:   
        cart = Cart.objects.get(user=request.user)
        print(cart.cartitems.all())
        username = request.user.username
        email = request.user.email
        mobile = Mobile.objects.get(user=request.user)
        phone_no = mobile.phone_no
        food_list = []
        food_model = ContentType.objects.get(model="food")
        soup_model = ContentType.objects.get(model="soup")
    
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItemsFood.objects.filter(cart=cart)
                                                                                                                                         
        for item in cart_items:
            if item.content_type == food_model:
                id = item.object_id
                content_type = item.content_type
                food = Food.objects.get(pk=id)
                quantity = item.quantity
                food_category = item.food_category
                total_food_price = item.total_price()
                item_list = [id,content_type,food,quantity,food_category,total_food_price]
                food_list.append(item_list)
            else:
                id = item.object_id
                content_type = item.content_type
                food = Soup.objects.get(pk=id)
                quantity = item.quantity
                food_category = item.food_category
                soup_price = item.soup_price()
                total_food_price = item.total_price()
                item_list = [id,content_type,food,quantity,food_category,soup_price,total_food_price]
                food_list.append(item_list)
              
        total_quantities = item.all_food_and_soup_quantities()
        total_price = item.all_soup_and_food_prices()
    except Cart.DoesNotExist:
        messages.info(request,"Add items to cart to view items!")
        return redirect('home')
    
    return render(request,'cart/cart-items.html',{'cart':cart,'tx_ref':tx_ref(),'items':food_list,'food_model':food_model,'soup_model':soup_model,
                                                  'total_quantities':total_quantities,'total_price':total_price,
                                                  'username':username,'email':email,'phone_no':phone_no})
'''   


def cart_buttons(request):
    new_item = ""
    try:
        data = json.loads(request.body)
        object_id = data['id']
        name = data['btn_name']
        form = data['form']
        
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItemsFood.objects.filter(cart=cart)
        for item in cart_items:
            total_quantities = item.all_food_and_soup_quantities()
        total_quantities = total_quantities
        
        if name == "add-item":
            item = cart_items.get(object_id=object_id)
            item.quantity += 1
            item.save()
            new_item = item.quantity
        elif name == "subtract-item":
            item = cart_items.get(object_id=object_id)
            item.quantity -= 1
            item.save()
            if item.quantity < 1:
                item.delete()
            new_item = item.quantity
        else:
            item = cart_items.get(object_id=object_id)
            new_item = item.delete()
    except:
        pass
    
    return JsonResponse(new_item, safe=False)

