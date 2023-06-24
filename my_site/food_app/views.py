from django.http import Http404
from django.shortcuts import redirect,render
from food_app.models import Food, Soup
from payments.forms import PaymentForm
from cart.models import Cart,CartItemsFood,CartItemsSoup
from django.contrib import messages
from django.http.response import JsonResponse,HttpResponse
import json


# Create your views here.

#what food box function does is, first, I used a for loop on the model Food, then listed all the field in the models
#such as: image,food_item,food_price and food slug. put the=m in a list
#and then append them into a list and did the same for all the objects in the model.

def food_box_func():
    my_food_box = Food.objects.all()

    append_list_item = []
    for item in my_food_box:
        pk = item.pk
        image = item.image
        food_item = item.food_item
        food_price = item.food_price
        food_slug = item.slug
        list_item = [image,food_item,food_price,food_slug,pk]
        new_list_item = append_list_item.append(list_item)
    return append_list_item


def soup_box_func():
    my_soup_box = Soup.objects.all()

    append_list_item2 = []
    for item in my_soup_box:
        pk = item.pk
        image = item.image
        soup_item = item.soup_item
        mini = item.mini_box
        medium = item.medium_box
        mega = item.mega_box
        slug = item.slug
        list_item2 = [image,soup_item,mini,medium,mega,slug,pk]
        new_list_item2 = append_list_item2.append(list_item2)
    return append_list_item2



def food_box(request):

    return render(request,'food_app/food_box.html',{'item':food_box_func()})    


def soup_box(request):
    
    return render(request,'food_app/soup_box.html',{'item2':soup_box_func()})



def add_to_cart(request):
    cart_object = ""
    product = ""
    product2 = ""
    data = json.loads(request.body)
    product_id = data['id']
    product = Food.objects.get(pk=product_id)   
    #product2 = Soup.objects.get(pk=product_id) 
    
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user,is_paid=False)
            
        cart_user = Cart.objects.get(user=request.user)
        cartitems = CartItemsFood.objects.get_or_create(cart=cart_user,product=product)
        
        #cartitems2 = CartItemsSoup.objects.get_or_create(cart=cart_user,product=product2)

        cart_object = CartItemsFood.objects.get(product=product,cart=cart_user)
        cart_object.quantity += 1
        cart_object.save()
        #else:
        #    cart_object2 = CartItemsSoup.objects.get(product=product2,cart=cart_user)
        #    cart_object2.quantity += 1
        #   cart_object2.save()

    return JsonResponse("i am now working!",safe=False)

