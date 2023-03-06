from django.urls import path 
from .import views 



app_name = 'cart'



urlpatterns = [
    path('add/<slug:slug>',views.cart_add,name='cart_add'),
    path('delete/<slug:slug>',views.cart_delete,name='cart_delete'),
]
