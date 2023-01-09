from django.shortcuts import render
from food_app.models import Food, Soup
from food_app.views import food_box_func,soup_box_func
# Create your views here.


#What I did here is that I called the food and soup model function, then I looped through the items,
#Set an if-statement condition so that once the price and slug request == any of the particular request item, 
# it returns the item objects in the front end  


def payment(request, price, slug):
    
    try:
        for item in food_box_func():
            if price == item[2] and slug == item[3]:
                break
    except:
        pass

    try:
        for item2 in soup_box_func():
            if price == item2[2] and slug == item2[5] or price == item2[3] and slug == item2[5] or price == item2[4] and slug == item2[5] or price == 11 and slug == item2[5]:
                break
    except:
        pass
    return render(request,'payments/pay.html',{'price':price,'slug':slug,'item':item,'item2':item2})
    
'''   
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
            if price == list_item2[2] and slug == list_item2[5] or price == list_item2[3] and slug == list_item2[5] or price == list_item2[4] and slug == list_item2[5] or price == 11 and slug == list_item2[5]:
                break
            
    except: 
        pass

    return render(request,'payments/pay.html',{'price':price,'slug':slug,'item':list_item,'item2':list_item2})
'''

