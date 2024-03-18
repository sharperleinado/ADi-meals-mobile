from django.contrib import admin
from django.urls import path,include ,re_path
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from cart.models import CartItemsFood,Cart
from django.http import HttpResponse

def home(request):
    
    return render(request,'home.html',{})

def profile(request):

    return render(request,'profile.html',{})

def about(request):
    
    return render(request,'about.html',{})
def contact(request):
    
    return render(request,'contact.html',{})
def foods(request):
    return render(request,'foods.html',{})
def cart(request):
    return render(request,'cart.html',{})
    
def soups(request):
    
    return render(request,'soupcategory.html',{})


def category(request, slug):
    context = {
            'slug': slug,
        }
    return render(request, 'foods.html', context)

def selecteditem(request, slug):
    context = {
            'slug': slug,
        }
    return render(request, 'selected-food.html', context)

urlpatterns = [
    re_path(r'^category/(?P<slug>[\w\s-]+)/$', category, name="category"),
    re_path(r'^selecteditem/(?P<slug>[\w-]+)/$', selecteditem, name="selecteditem"),
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
    path('soups/',soups,name='soups'),
    path('contact/',contact,name='contact'),
    path('cart/',cart,name='cart'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
