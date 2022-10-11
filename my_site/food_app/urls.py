from django.urls import path
from. import views


app_name = 'food_app'


urlpatterns = [
    path('food_box/',views.food_box,name='foodbox'),
    path('soup_box/',views.soup_box,name='soupbox'),
    path('price_in_packs/',views.price_in_packs,name='price'),
]
