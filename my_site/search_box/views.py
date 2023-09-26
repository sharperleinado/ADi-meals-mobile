from asyncio.windows_events import NULL
from tkinter.tix import FileEntry
from django.shortcuts import render,redirect
from food_app.models import Food,Soup
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

# Create your views here.


def search_box(request):
    search_box = ""
    food_box = ""
    soup_box = ""
    search_list = ""
    try:
        if request.method == "POST":
            search_box = request.POST.get("search").strip()
            #food  = ContentType.objects.get()
            food_box = Food.objects.filter(food_item__contains = search_box).all()
            soup_box = Soup.objects.filter(soup_item__contains = search_box).all()
            search_list = [search_box,food_box,soup_box]
    except:
        pass

    return render(request,'search_box/search.html',{'searched':search_box,'food':food_box,'soup':soup_box,
    'search_list':search_list})
    

#Food_search renders all the food and soup search on a different template and accepts a slug request when sent from the user
#which filters the provided slug in the model and display the object model searched by the user to the user.
def food_result(request,slug):
    my_food_box = ""
    my_soup_box = ""
    price = 11
    
    try:
        my_food_box = Food.objects.get(slug=slug)
    except:
        pass

    try:
        my_soup_box = Soup.objects.get(slug=slug)
    except:
        pass

    return render(request,'food_app/food_search.html',{'price':price,'item':my_food_box,'item2':my_soup_box}) 
