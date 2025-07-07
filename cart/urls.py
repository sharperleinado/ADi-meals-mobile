from django.urls import path 
from .import views 



app_name = 'cart'



urlpatterns = [
    path('cart-items/',views.cart_items,name='cart_items'),
    path('cart-buttons/',views.cart_buttons,name='cart_buttons'),
    path('clear_all/',views.clear_all,name='clear_all'),
    path('change_cart_protein/',views.change_cart_protein,name='change_cart_protein'),
]
