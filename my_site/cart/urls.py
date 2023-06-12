from django.urls import path 
from .import views 



app_name = 'cart'



urlpatterns = [
    path('cart-items/',views.cart_items,name='cart_items'),
]
