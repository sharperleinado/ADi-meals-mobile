from django.http import Http404
from django.shortcuts import render
from food_app.models import Food,Soup
from django.http import Http404


# Create your views here.


def search_box(request):
    if request.method == "GET":
        search_box = request.GET.get("search")
        food_box = Food.objects.filter(food_item__startswith = search_box).all()
        soup_box = Soup.objects.filter(soup_item__startswith = search_box).all()

        my_dict = {'food':food_box,'soup':soup_box}

        return render(request,'search_box/search.html',context=my_dict)

    else:
        return render(request,'search_box/search.html')
   