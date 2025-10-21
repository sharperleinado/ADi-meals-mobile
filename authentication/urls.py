from django.urls import path
from . import views



app_name = 'authentication'



urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('activate/<uidb64>/<token>/<str:resetoractivate>/<otp>',views.activate,name='activate'),
    path('account_info/',views.account_info,name='account_info'),
    path('edit_account/',views.edit_account,name='edit_account'), 
    path('forgetpassword/',views.forgetpassword,name='forgetpassword'),#Interface that leads to forgetpassword
    path('reset/<uid>/<token>',views.password_reset,name='reset'),
    path('otp/',views.otp,name='otp'),
    path('change_address/',views.change_address,name='change_address'),
    path('change_address_division/',views.change_address_division,name='change_address_division'),
    path('change_address_lga/',views.change_address_lga,name='change_address_lga'),
]


