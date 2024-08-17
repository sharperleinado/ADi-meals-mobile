from django.urls import path
from. import views


app_name = 'food_app'


urlpatterns = [
    path('food_box/',views.food_box,name='foodbox'),
    path('soup_box/',views.soup_box,name='soupbox'),
    path('add_to_cart/',views.add_to_cart,name='addtocart'),
    path('change_protein/',views.change_protein,name='change_protein'),
] 
