"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include 
from django.shortcuts import render
from django.contrib.auth.models import User 
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from food_app.views import food_box_func


def home(request):
    fname=""
    try:
        fname = request.user.first_name
    except:
        pass

    return render(request,'home.html',{'fname':fname})


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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
