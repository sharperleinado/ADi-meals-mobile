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
    

