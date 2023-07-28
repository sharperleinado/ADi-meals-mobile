from django.urls import path,register_converter
from . import views,converters

register_converter(converters.FloatUrlParameterConverter, 'float')




app_name = 'payments'



urlpatterns = [
    path('payment-page/<float:price>/<slug:slug>/',views.payment,name='payment'), #This is for payment page
    path('price/<slug:slug>/',views.price_in_pack,name='price'), #This is for price in pack page
    path('payment_api/',views.payment_api,name='payment_api'), #This is going to be for paystack
    path('add_to_cart/',views.add_to_cart,name='addtocart'),
]

