from django.shortcuts import render
from food_app.views import food,soup
from django.http.response import JsonResponse,HttpResponse
import json
from cart.models import Cart,CartItemsFood
from django.contrib.contenttypes.models import ContentType
from authentication.models import Mobile
import math
import random
from my_site.settings import get_env_variable
import requests
# Create your views here.



#What I did here is that I called the food and soup model function, then I looped through the items,
#Set an if-statement condition so that once the price and slug request == any of the particular request item, 
# it returns the item objects in the front end  
def payment(request, price, slug):
    username = request.user.username
    email = request.user.email
    mobile = Mobile.objects.get(user=request.user)
    phone_no = mobile.phone_no
    item = ""
    item2 = ""   
    
    def tx_ref():
        tx_ref = ''+str(math.floor(1000000 + random.random()*9000000))
        return  tx_ref
    
    try:
        for item in food:
            if price == item.food_price and slug == item.slug:
                break
        item = item
        print(item.__class__)
    except:
        pass
    
    try:
        for item2 in soup:
            if price == item2.mini_box_price and slug == item2.slug or price == item2.medium_box_price and slug == item2.slug or price == item2.mega_box_price and slug == item2.slug or price == 11 and slug == item2.slug:
                break
        item2 = item2
    except:
        pass

    return render(request,'payments/pay.html',{'tx_ref':tx_ref,'price':price,'slug':slug,'item':item,'item2':item2,'email':email,'username':username,'phone_no':phone_no})


#What I did here is, I first got the price_in_pack input from the user,
#Then if the slug request taken from the price_in_pack form is equal to the slug in the price_in_pack, the program breaks out of the loop and return the view to the user 
def price_in_pack(request, slug):
    total_price = ""
    quantity = ""
    item = ""
    if request.method == "POST":
            try:
                quantity = int(request.POST.get("quantity"))
                for item in food:
                    if slug == item.slug:
                        break
                    item = item
                total_price = quantity*item.food_price
            except ValueError:
                return render(request,'food_app/404.html')
            except:
                return render(request,'food_app/404.html')

    return render(request,'payments/price.html',{'slug':slug,'quantity':quantity,'total_price':total_price,'item':item})



def flutter_api(request,username,email,phone_no,price):
    auth_token= get_env_variable('SECRET_KEY')#env('SECRET_KEY')
    hed = {'Authorization': f"Bearer {auth_token}"}
    data = {
            "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
            "amount":price,
            "currency":"NGN",
            "redirect_url":"http://localhost:8000/payments/verify_payment",
            "payment_options":"card, ussd, mobilemoneynigeria",
            "meta":{
                "consumer_id":23,
                "consumer_mac":"92a3-912ba-1192a"
            },
            "customer":{
                "email":email,
                "phonenumber":phone_no,
                "name":username
            },
            "customizations":{
                "title":"ADi meals limited",
                "description":"Your Number one Food and Soup service",
                "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
            }
            }
    url = 'https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response_data=response.json()
    link=response_data['data'], response_data['link']
    return link

def verify_payment(request, pk):
    
    return HttpResponse("finished")


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = soup.get(pk=product_id)   
    id = product.pk
    product_price = data['price']
    
    
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user,is_paid=False)
            
        cart_user = Cart.objects.get(user=request.user)
        content = ContentType.objects.get_for_model(product)
        cartitems = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,object_id=id,food_category=product_price)
        
        cart_object = CartItemsFood.objects.get(cart=cart_user,content_type=content,object_id=id,food_category=product_price)
        cart_object.quantity += 1
        cart_object.save()   
        
        num_of_items = cart_object.all_food_and_soup_quantities()
        
    return JsonResponse(num_of_items,safe=False)

    