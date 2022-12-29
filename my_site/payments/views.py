from django.shortcuts import render
from food_app.models import Food, Soup
from food_app.views import food_box_func,soup_box_func
# Create your views here.






def payment(request, slug):


    
    return render(request,'payments/pay.html',{'food':food_box_func(),'soup':soup_box_func()})



