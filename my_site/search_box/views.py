from asyncio.windows_events import NULL
from tkinter.tix import FileEntry
from django.shortcuts import render,redirect
from food_app.models import Food,Soup


# Create your views here.


def search_box(request):

    if request.method == "GET":
        search_box = request.GET.get("search")
        food_box = Food.objects.filter(food_item__startswith = search_box).all()
        soup_box = Soup.objects.filter(soup_item__startswith = search_box).all()

        return render(request,'search_box/search.html',{'food':food_box,'soup':soup_box})

        
   