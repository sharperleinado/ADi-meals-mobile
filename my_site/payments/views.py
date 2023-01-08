from django.shortcuts import render
from food_app.models import Food, Soup
from food_app.views import food_box_func,soup_box_func
# Create your views here.


#What I did here is that I looped  through all products in the food and soup model,
#Then asked the program to check if the slug request from the user is the paticular object slug
# if it is, it should break out of the loop and list the object item. 

def payment(request, price, slug):
    
    try:
        my_food_box = Food.objects.all()

        for item in my_food_box:
            image = item.image
            food_item = item.food_item
            food_price = item.food_price
            food_slug = item.slug
            list_item = [image,food_item,food_price,food_slug]
            if price == list_item[2] and slug == list_item[3]:
                break
    except:
        pass

    try:
        my_soup_box = Soup.objects.all()

        for item in my_soup_box:
            image = item.image
            soup_item = item.soup_item
            soup_mini = item.mini_box
            soup_medium = item.medium_box
            soup_mega = item.mega_box
            soup_slug = item.slug
            list_item2 = [image,soup_item,soup_mini,soup_medium,soup_mega,soup_slug]
            if price == list_item2[2] and slug == list_item2[5] or price == list_item2[3] and slug == list_item2[5] or price == list_item2[4] and slug == list_item2[5]:
                break
            
    except: 
        pass

    return render(request,'payments/pay.html',{'price':price,'slug':slug,'item':list_item,'item2':list_item2})


