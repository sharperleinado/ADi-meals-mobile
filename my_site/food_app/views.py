from django.http import Http404
from django.shortcuts import redirect,render
from food_app.models import Food, Soup
from payments.forms import PaymentForm
from cart.models import Cart,CartItemsFood
from django.contrib import messages
from django.http.response import JsonResponse,HttpResponse
import json
from django.contrib.contenttypes.models import ContentType



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
        mini_name = item.mini_box_name
        mini_price = item.mini_box_price
        medium_name = item.medium_box_name
        medium_price = item.medium_box_price
        mega_name = item.mega_box_name
        mega_price = item.mega_box_price
        slug = item.slug
        uuid = item.uid
        list_item2 = [image,soup_item,mini_name,mini_price,medium_name,medium_price,mega_name,mega_price,slug,pk,uuid]
        new_list_item2 = append_list_item2.append(list_item2)
    return append_list_item2



def food_box(request):

    return render(request,'food_app/food_box.html',{'item':food_box_func()})    


def soup_box(request):
    
    return render(request,'food_app/soup_box.html',{'item2':soup_box_func()})



def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = Food.objects.get(pk=product_id) 
    id = product.pk
    
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user,is_paid=False)
            
        cart_user = Cart.objects.get(user=request.user)
        content = ContentType.objects.get_for_model(product)
        cartitems = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,object_id=id)

        cart_object = CartItemsFood.objects.get(cart=cart_user,content_type=content,object_id=id)
        cart_object.quantity += 1
        cart_object.save()

    return JsonResponse("i am now working!",safe=False)

