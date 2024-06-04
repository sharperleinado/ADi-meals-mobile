from django import views
from django.urls import path
from . import views 


app_name = 'search_box'



urlpatterns = [
    path('search/',views.search_box,name='search'),
    path('food_result/<slug:slug>/',views.food_result,name='food_result'),
    path('add_to_cart/',views.add_to_cart,name='addtocart'),
]