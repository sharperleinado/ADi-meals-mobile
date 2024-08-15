from django.urls import path
from . import views


app_name = "address"


urlpatterns = [
    path('register_address/',views.register_address,name="register_address"),
    path('billing_address/',views.billing_address,name="billing_address"),
    #path('update_address/',views.update_address,name="update_address"),
    path('change_address/',views.change_address,name='change_address'),
    path('change_address_division/',views.change_address_division,name='change_address_division'),
    path('change_address_lga/',views.change_address_lga,name='change_address_lga'),
]
