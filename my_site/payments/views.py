from django.shortcuts import render,redirect
from django.http.response import JsonResponse,HttpResponse
import json
from cart.models import Cart,CartItemsFood
from django.contrib.contenttypes.models import ContentType
from authentication.models import Mobile
import math
import random
#from my_site.settings import get_env_variable
import requests
from food_app.views import food,soup
from django.db.models import Q
import uuid
from address.models import UserAddress
from django.contrib import messages

# Create your views here.




def tx_ref():
    tx_ref = ''+str(math.floor(1000000 + random.random()*9000000))
    return  tx_ref



def payment(request, price, slug):
    email = ""
    username = ""
    mobile = ""
    phone_no = ""
    try:
        if request.user.is_authenticated:
            address = UserAddress.objects.get(user=request.user)
            username = request.user.username
            email = request.user.email
            mobile = Mobile.objects.get(user=request.user)
            phone_no = mobile.phone_no
            print(phone_no)
        else:
            address = "Anonymousstreet.com"
            username = "Anonymous User"
            email = "Anonymoususer@gmail.com"
            phone_no = "081-Anonymous User"
            print(phone_no)
            print(address)
            
    except Mobile.DoesNotExist:
        messages.error(request, "Please, complete Account Information before proceeding")
        return redirect('authentication:account_info')
    
    def get_food_item():
        return food.filter(food_price=price, slug=slug).first()

    def get_soup_item():
        return soup.filter(Q(mini_box_price = price) & Q(slug = slug) | Q(medium_box_price = price) & Q(slug = slug) | Q(mega_box_price = price) & Q(slug = slug) | Q(pk = price) & Q(slug = slug)).first()

    return render(request, 'payments/checkout.html', {
        'item': get_food_item(),
        'item2': get_soup_item(),
        'tx_ref': tx_ref,
        'price': price,
        'slug': slug,
        'email': email,
        'username': username,
        'phone_no': phone_no,
        #'address':address,
    })


#What I did here is, I first got the price_in_pack input from the user,
#Then if the slug request taken from the price_in_pack form is equal to the slug in the price_in_pack, the program breaks out of the loop and return the view to the user 
def price_in_pack(request, slug):
    total_price = ""
    quantity = ""
    item = ""
    if request.method == "POST":
            try:
                mobile = Mobile.objects.get(user=request.user)
                phone_no = mobile.phone_no
                quantity = int(request.POST.get("quantity"))
                food_item = food.get(slug=slug)
                total_price = quantity*food_item.food_price
            except ValueError:
                return render(request,'food_app/404.html')
            except:
                return render(request,'food_app/404.html')

    return render(request,'payments/price.html',{'slug':slug,'quantity':quantity,'total_price':total_price,'item':item,'tx_ref':tx_ref,'email':request.user.email,'username':request.user.username,'phone_no':phone_no})


'''
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
    return link'''

def verify_payment(request, pk, item):
    print(pk)
    print(item)
    
    return HttpResponse("finished")


def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data['id']
        product = soup.get(pk=product_id)   
        id = product.pk
        product_price = data['price']
    
    
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user,is_paid=False)
            
            cart_user = Cart.objects.get(user=request.user)
            content = ContentType.objects.get_for_model(product)
            cartitems, created = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,object_id=id,food_category=product_price)
        
            cartitems.quantity += 1
            cartitems.save()   
            num_of_items = cart.total_quantity()
        else:
            try:
                cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                content = ContentType.objects.get_for_model(product)
                cartitems, created = CartItemsFood.objects.get_or_create(cart=cart,content_type=content,object_id=id,food_category=product_price)
                
                cartitems.quantity += 1
                cartitems.save()
                num_of_items = cart.total_quantity()
            except:
                request.session['cart_users'] = str(uuid.uuid4())
                cart = Cart.objects.create(session_id=request.session['cart_users'],is_paid=False)
                cart_user = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                content = ContentType.objects.get(model="soup")
                cartitems, created = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,object_id=id,food_category=product_price)
                
                cartitems.quantity += 1
                cartitems.save()
                num_of_items = cart_user.total_quantity()

    except:
        pass
    return JsonResponse(num_of_items,safe=False)

    