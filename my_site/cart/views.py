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

    #new_food = []
    #new_soup = []
    #food_total = []
    #soup_total = []
    #food_total_2 = []
    #soup_total_2 = []
    #food_model = ContentType.objects.get(model="food")
    #soup_model = ContentType.objects.get(model="soup")
    #try:
    #    cart = Cart.objects.get(user=request.user)
    #    items_in_cart = CartItemsFood.objects.filter(cart=cart)
    #   
    #    for item in items_in_cart:
    #        if item.content_type == food_model:
    #            quantity = item.quantity
    #            id = item.object_id
    #            content_type = item.content_type
    #            food = Food.objects.get(pk=id)
    #            food_image = food.image
    #            food_item = food.food_item
    #            food_price = food.food_price
    #            food_total.append(quantity)
    #            
    #            def total_quantity():
    #                new_quantity = quantity*food_price
    #                return new_quantity
    #    
    #            food_total_2.append(total_quantity())
    #            list_items = [food_image,food_item,food_price,quantity,total_quantity(),content_type]
    #            new_food.append(list_items)
    #
    #        else:
    #            quantity_2 = item.quantity
    #            id = item.object_id
    #            content_type_2 = item.content_type
    #            soup = Soup.objects.get(pk=id)
    #            soup_image = soup.image
    #            soup_item = soup.soup_item
    #            soup_mini = soup.mini_box
    #            soup_medium = soup.medium_box
    #            soup_mega = soup.mega_box
    #            food_total.append(quantity_2)
    #                
    #            list_items = [soup_image,soup_item,quantity_2,content_type_2]
    #            new_food.append(list_items)
    # 
    #    sum_of_new_total = sum(food_total)
    #    sum_of_new_total_2 = sum(food_total_2)
    
    #except:
    #    messages.info(request, "No items in cart! Add items to cart to view cart items!")
    #    return redirect('home')

    #return render(request,'cart/cart-items.html',{'soup_model':soup_model,'food_model':food_model,'items':new_food,'new_sum':sum_of_new_total,'new_sum2':sum_of_new_total_2})
    return render(request,'cart/cart-items.html',{'items':food_list,'food_model':food_model,'soup_model':soup_model})

