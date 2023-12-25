from django.contrib import admin
from django.urls import path,include 
from django.shortcuts import render
from django.contrib.auth.models import User 
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from cart.models import CartItemsFood,Cart



def home(request):
    fname = ""
    cart = ""
    cart_total = ""
    try:
        fname = request.user.first_name
    except:
        pass
    
    try:
        cart = Cart.objects.get(user=request.user)
        cart_total = cart.total_quantity()
    except:
        cart_total = 0
        pass

    return render(request,'home.html',{'fname':fname,'cart':cart_total})


def profile(request):
    fname=""
    try:
        fname = request.user.first_name
    except:
        pass
    
    try:
        cart = Cart.objects.get(user=request.user)
        cart_total = cart.total_quantity()
    except:
        cart_total = 0
        pass

    return render(request,'profile.html',{'cart':cart_total,'fname':fname})

def about(request):
    
    return render(request,'about.html',{})
     
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
    path('about/',about,name='about'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
