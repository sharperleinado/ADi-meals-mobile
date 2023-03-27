from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from food_app.models import Food,Soup
from django.contrib import messages
from django.shortcuts import redirect
from .models import CartItemsFood,Cart

# Create your views here.


def cart_items(request): 
    items_in_cart = CartItemsFood.objects.all()
    length = len(items_in_cart)
    if request.method == "POST":
        add = request.POST.get("add")
        subtract = request.POST.get("subtract")
        slug = request.POST.get("slug")
        if add:
            model = CartItemsFood.objects.get(pk=slug)
            model.quantity += 1
            current_price = model.product.food_price * model.quantity
            model.save()
        elif subtract:
            model = CartItemsFood.objects.get(pk=slug)
            model.quantity -= 1
            if model.quantity < 0:
                model.delete()
                messages.error(request, "You have delted item from cart!")
                return redirect('cart:cart_items')
            model.save()

    return render(request,'cart/cart-items.html',{'items':items_in_cart,'len':length})

