from django.urls import path,register_converter
from . import views,converters

register_converter(converters.FloatUrlParameterConverter, 'float')



app_name = 'payments'



urlpatterns = [
    path('payment/<float:price>/<slug:slug>/',views.payment,name='payment'),#This is for payment page
    path('price/<slug:slug>/',views.price_in_pack,name='price'), #This is for price in pack page
    path('add_to_cart/',views.add_to_cart,name='addtocart'),
    path('flutterwave/<str:username>/<str:email>/<str:phone_no>/<float:price>/<int:pk>/<slug:slug>', views.flutterwave, name='flutterwave'),
    path('verify_payment/<float:price>/<int:pk>/<slug:slug>',views.verify_payment,name='verify_payment'),
    path('transactions/',views.transactions,name='transactions'),
]
