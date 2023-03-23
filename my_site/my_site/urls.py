from django.contrib import admin
from django.urls import path,include 
from django.shortcuts import render
from django.contrib.auth.models import User 
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from food_app.views import food_box_func
from cart.models import CartItemsFood


def home(request):
    fname=""
    try:
        fname = request.user.first_name
    except:
        pass
    items_in_cart = CartItemsFood.objects.all()
    length = len(items_in_cart)

    return render(request,'home.html',{'fname':fname,'len':length})


def profile(request):
    fname=""
    try:
        fname = request.user.first_name
    except:
        pass

    return render(request,'profile.html',{'fname':fname})

     
urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/',include('authentication.urls')),
    path('food_app/',include('food_app.urls')),
    path('',home,name='home'),
    path('search/',include('search_box.urls')),
    path('payments/',include('payments.urls')),
    path('profile/',profile,name='profile'),
    path('address/',include('address.urls')),
    path('review/',include('review.urls')),
    path('cart/',include('cart.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
