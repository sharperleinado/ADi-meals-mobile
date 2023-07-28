from django.shortcuts import render
from food_app.models import Food,Soup
from django.contrib import messages
from django.shortcuts import redirect
from .models import CartItemsFood,Cart
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

# Create your views here.


def cart_items(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items_in_cart = CartItemsFood.objects.filter(cart=cart)

        new_food = []
        new_soup = []
        food_total = []
        soup_total = []
        food_total_2 = []
        soup_total_2 = []
        for item in items_in_cart:
            food_model = ContentType.objects.get(model="food")
            soup_model = ContentType.objects.get(model="food")
            if item.content_type == food_model:
                quantity = item.quantity
                id = item.object_id
                food = Food.objects.get(pk=id)
                food_image = food.image
                food_item = food.food_item
                food_price = food.food_price
                food_total.append(quantity)
                
                def total_quantity():
                    new_quantity = quantity*food_price
                    return new_quantity

                food_total_2.append(total_quantity())
                    
                list_items = [food_image,food_item,food_price,quantity,total_quantity()]
                new_food.append(list_items)

            else:
                quantity_2 = item.quantity
                id = item.object_id
                soup = Soup.objects.get(pk=id)
                soup_image = soup.image
                soup_item = soup.soup_item
                soup_mini = soup.mini_box
                soup_medium = soup.medium_box
                soup_mega = soup.mega_box
                soup_total.append(quantity)
                
                def mini(*args):
                    if args == "mini":
                        return list(soup_image,soup_item,soup_mini)
                
                def medium(*args):
                    if args == "medium":
                        return list(soup_image,soup_item,soup_medium)
                
                def mega(*args):
                    if args == "mega":
                        return list(soup_image,soup_item,soup_mega)
                #def mini_box():
                #    new_quantity = quantity*soup_mini
                #    return new_quantity
                
                #def medium_box():
                #    new_quantity = quantity*soup_medium
                #    return new_quantity
                
                #def mega_box():
                #    new_quantity = quantity*soup_mega
                #    return new_quantity

                #soup_total_2.append(mini_box())
                    
                #list_items_2 = [soup_image,soup_item,quantity]
                #new_soup.append(list_items_2)

        sum_of_new_total = sum(food_total)
        sum_of_new_total_2 = sum(food_total_2)
        
    except:
        messages.info(request, "No items in cart! Add items to cart to view cart items!")
        return redirect('home')

    return render(request,'cart/cart-items.html',{'items':new_food,'items_2':new_soup,'new_sum':sum_of_new_total,'new_sum2':sum_of_new_total_2})

