from django.http import Http404
from django.shortcuts import redirect,render
from food_app.models import Food, Soup
from django.urls import reverse

# Create your views here.


def slug_view():
    my_food_box = Food.objects.all()

    append_list_item3 = []
    for item in my_food_box:
        food_slug = item.slug
        new_append = append_list_item3.append(food_slug)
    return append_list_item3


def slug_view2():
    my_soup_box = Soup.objects.all()

    append_list_item3 = []
    for item in my_soup_box:
        soup_slug = item.slug
        new_append = append_list_item3.append(soup_slug)
    return append_list_item3


#what food box function does is, first, I used a for loop on the model Food, then listed all the field in the models
#such as: image,food_item,food_price and food slug. put the=m in a list
#and then append them into a list and did the same for all the objects in the model.
def food_box_func():
    my_food_box = Food.objects.all()

    append_list_item = []
    for item in my_food_box:
        image = item.image
        food_item = item.food_item
        food_price = item.food_price
        food_slug = item.slug
        list_item = [image,food_item,food_price,food_slug]
        new_list_item = append_list_item.append(list_item)
    return append_list_item


def soup_box_func():
    my_soup_box = Soup.objects.all()

    append_list_item2 = []
    for item in my_soup_box:
        image = item.image
        soup_item = item.soup_item
        mini = item.mini_box
        medium = item.medium_box
        mega = item.mega_box
        slug = item.slug
        list_item2 = [image,soup_item,mini,medium,mega,slug]
        new_list_item2 = append_list_item2.append(list_item2)
    return append_list_item2




def food_box(request, slug):
    
    
        
    if request.method == "POST":

        try:
            item1 = int(request.POST.get("price in pack"))
            print(item1)
            #return reverse('payments':'payment')
        except ValueError:
            return render(request,'food_app/404.html')
    
        
    return render(request,'food_app/food_box.html',{'item':food_box_func()})



def soup_box(request, slug):

    
    return render(request,'food_app/soup_box.html',{'item2':soup_box_func()})

