from django.contrib import admin
from django.urls import path,include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static



def home(request):
    
    return render(request,'home.html',{})

def profile(request):

    return render(request,'profile.html',{})

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
