from django.contrib import admin
from .models import Cart
from cart.models import CartItemsFood

# Register your models here.



admin.site.register(Cart)
admin.site.register(CartItemsFood)
