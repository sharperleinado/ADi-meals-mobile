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
        new_total = []
        new_total_2 = []
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
                new_total.append(quantity)
                
                def total_quantity():
                    new_quantity = quantity*food_price
                    return new_quantity

                new_total_2.append(total_quantity())
                    
                list_items = [food_image,food_item,food_price,quantity,total_quantity()]
                new_food.append(list_items)

            else:
                pass

        sum_of_new_total = sum(new_total)
        sum_of_new_total_2 = sum(new_total_2)

    except:
        messages.info(request, "No items in cart! Add items to cart to view cart items!")
        return redirect('home')

    return render(request,'cart/cart-items.html',{'items':new_food,'new_sum':sum_of_new_total,'new_sum2':sum_of_new_total_2})

