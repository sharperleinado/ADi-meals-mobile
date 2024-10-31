from django.contrib import admin
from django.urls import path,include ,re_path
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from cart.models import CartItemsFood,Cart
from django.http import HttpResponse

def home(request):
    fname = ""
    try:
        if request.user.is_authenticated:
            fname = request.user.first_name

            new = request.session.get('cartitems')
            del new 
    except AttributeError:
        pass
    
    return render(request,'home_kunkky.html',{'fname':fname})

def profile(request):
    fname = ""
    lname = ""

    try:
        if request.user.is_authenticated:
            fname = request.user.first_name
            lname = request.user.last_name
        else:
            fname = "Prospective"
            lname = "Customer"
    except AttributeError:
        pass

    return render(request,'profile.html',{'fname':fname,'lname':lname})

def about(request):
    
    return render(request,'about.html',{})

def contact(request):
    
    return render(request,'contact.html',{})

def base(request):

    return render(request,'base/base.html',{})

def terms_of_service(request):

    return render(request,'terms_of_service.html')

def privacy_policy(request):

    return render(request,'privacy_policy.html')
    

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
    path('accounts/',include('allauth.urls')),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('base/',base,name='base'),
    path('terms_of_service/',terms_of_service,name='terms_of_service'),
    path('privacy_policy/',privacy_policy,name='privacy_policy'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)