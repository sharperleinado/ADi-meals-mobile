from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from food_app.models import Food,Soup
from django.contrib import messages
from django.shortcuts import redirect
from .models import CartItemsFood,Cart
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.


def cart_items(request):
    
    cart = Cart.objects.get(user=request.user)
    try:
        items_in_cart = CartItemsFood.objects.filter(cart=cart)

        new = []
        for item in CartItemsFood.objects.all():
            new_sum = new.append(item.total_quantity)
        for item in new:
            new_sum1 = sum(new)
        print(new_sum1)
    except:
        messages.info(request, "No items in cart! Add items to cart to view cart items!")
        return redirect('home')


    return render(request,'cart/cart-items.html',{'items':items_in_cart,'new':new_sum1})

    
'''    
    length = len(items_in_cart)
    if length < 1:
        cart.delete()
        return redirect('cart:cart_items')


    if request.method == "POST":
        add = request.POST.get("add")
        subtract = request.POST.get("subtract")
        if add:
            model = items_in_cart.get(pk=add)
            model.quantity += 1
            model.product.food_price = model.total_quantity()
            model.save()
        elif subtract:
            model = CartItemsFood.objects.get(pk=subtract)
            model.quantity -= 1
            model.product.food_price = model.total_quantity()
            if model.quantity < 1:
                model.delete()
                messages.error(request, "You have deleted item from cart!")
                return redirect('cart:cart_items')
            else:
                model.save()
    '''
    
