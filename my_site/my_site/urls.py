from django.contrib import admin
from django.urls import path,include ,re_path
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from cart.models import CartItemsFood,Cart
from django.http import HttpResponse

def home(request):
    
    return render(request,'home_kunkky.html',{})

def profile(request):

    return render(request,'profile.html',{})

def about(request):
    
    return render(request,'about.html',{})

def base(request):
    
    return render(request,'base/base.html',{})



def contact(request):
    
    return render(request,'contact.html',{})

def cart(request):
    return render(request,'cart.html',{})
    

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
    path('contact/',contact,name='contact'),
    path('cart/',cart,name='cart'),
    path('base/', base, name="base")
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
