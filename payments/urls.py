from django.urls import path,register_converter
from . import views,converters

register_converter(converters.FloatUrlParameterConverter, 'float')



app_name = 'payments'



urlpatterns = [
    path('payment/<float:price>/<slug:slug>/',views.payment,name='payment'),#This is for payment page
    path('price/<slug:slug>/',views.price_in_pack,name='price'), #This is for price in pack page
    path('add_to_cart/',views.add_to_cart,name='addtocart'),
    path('flutterwave/<str:email>/<float:price>/<int:pk>/<slug:slug>/<float:delivery>', views.flutterwave, name='flutterwave'),
    path('paystack/<str:email>/<float:price>/<int:pk>/<slug:slug>/<float:delivery>', views.paystack, name='paystack'),
    path('verify_payment/<float:price>/<int:pk>/<slug:slug>/<float:delivery>',views.verify_payment,name='verify_payment'),
    path('all_transactions/',views.all_transactions,name='all_transactions'),
    path('change_protein/',views.change_protein,name='change_protein'),
    path('edit_account/<price>/<slug>/',views.edit_account,name='edit_account'),
    path('food_order_update/',views.food_order_update,name='food_order_update'),
]
