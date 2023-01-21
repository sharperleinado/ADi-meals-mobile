from django.urls import path
from . import views



app_name = 'payments'



urlpatterns = [
    path('<int:price><slug:slug>/',views.payment,name='payment'),
    path('<slug:slug>',views.price_in_pack,name='price'),
    path('payment_api/',views.payment_api,name='payment_api'),
]

