import datetime
from xmlrpc.client import DateTime
from django.shortcuts import render,redirect
from django.http.response import JsonResponse,HttpResponse
import json
from cart.models import Cart,CartItemsFood
from django.contrib.contenttypes.models import ContentType
from authentication.models import Mobile
import math
import random
from food_app.models import Food,Soup
import requests
from food_app.views import food, food_box,soup, soup_box
from django.db.models import Q
import uuid
from address.models import UserAddress
from django.contrib import messages
from django.urls import reverse
from food_app.views import food,soup
from django.http import JsonResponse
from my_site.settings import *
import os 
from dotenv import load_dotenv
from .models import Transactions
load_dotenv()

# Create your views here.

food_model = ContentType.objects.get(model="food")
soup_model = ContentType.objects.get(model="soup")
cart_model = ContentType.objects.get(model="cart")
cartitems_food = ContentType.objects.get(model="cartitemsfood")



def tx_ref():
    tx_ref = ''+str(math.floor(1000000 + random.random()*9000000))
    return  tx_ref


def flutterwave(request,username,email,phone_no,price,pk,slug):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {os.getenv('FLUTTERWAVE_SECRET_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "tx_ref": tx_ref(),
        "amount": float(price),
        "currency": "NGN",
        "redirect_url": f"http://localhost:8000/payments/verify_payment/{price}/{pk}/{slug}",#"http://localhost:8000/payments/verify_payment",
        "meta": {
            "consumer_id": 23,
            "consumer_mac": "92a3-912ba-1192a"
        },
        "customer": {
            "email": email,
            "phonenumber": str(phone_no),
            "name": username
        },
        "customizations": {
            "title": "ADi Meals Limited",
            "logo": "https://www.logolynx.com/images/logolynx/22/2239ca38f5505fbfce7e55bbc0604386.jpeg"#"https://imgur.com/a/KCgmWR2.jpg"#"https://www.dropbox.com/scl/fi/ocyprndvq10u9laropcjm/official-logo-design.jpg"
        },
        "configurations": {
            "session_duration": 10,  # Session timeout in minutes (maxValue: 1440 minutes)
            "max_retry_attempt": 5   # Max retry attempts for failed transactions
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        response.raise_for_status()  # Raise an error for bad status codes
 
        # Assuming the response is JSON, you can access it like this:
        json_response = response.json()
        print(json_response)
        if json_response['status'] == "success":
            generated_link = json_response['data']
            status = json_response['status']
            print(status)
            return redirect(generated_link['link'])
        
        return JsonResponse(json_response, safe=False)

    except requests.exceptions.RequestException as err:
        error_message = f"Error: {err}"
        return JsonResponse({"error": error_message}, status=500, safe=False)


def verify_payment(request,price,pk,slug):
    food_product = ""
    soup_product = ""
    cart = ""
    actual_price = ""
    actual_size = ""
    food_content = ""
    soup_content = ""
    cart_content = ""
    cartitems = ""
    new_cartitems = ""
    
    userprotein = request.session.get(str(request.user), ["beef", "fried beef"])

    if request.method == "GET":
        status = request.GET.get("status")
        tx_ref = request.GET.get("tx_ref")

        try:
            food_product = food.get(food_price=price,slug=slug,pk=pk)
            food_content = ContentType.objects.get_for_model(food_product)
            print(food_content)
            if status == "completed" and food_product is not None:
                user_transactions = Transactions.objects.create(user=request.user,boxsize="mini",protein=userprotein[0],subprotein=userprotein[1],status=status,amount=price,currency="NGN",tx_ref=tx_ref,content_type=food_content,object_id=pk)
            elif status == "failed" and food_product is not None:
                user_transactions = Transactions.objects.create(user=request.user,boxsize="mini",protein=userprotein[0],subprotein=userprotein[1],status=status,amount=price,currency="NGN",tx_ref=tx_ref,content_type=food_content,object_id=pk)
        except Food.DoesNotExist:
            pass

        try:
            soup_product = soup.get(slug=slug,pk=pk)
            soup_content = ContentType.objects.get_for_model(soup_product)
            if price == soup_product.mini_box_price:
                actual_price = soup_product.mini_box_price
                actual_size = soup_product.mini_box_name
            elif price == soup_product.medium_box_price:
                actual_price = soup_product.medium_box_price
                actual_size = soup_product.medium_box_name
            else:
                actual_price = soup_product.mega_box_price
                actual_size = soup_product.mega_box_name

            if status == "completed" and soup_product is not None:
                user_transactions = Transactions.objects.create(user=request.user,boxsize=actual_size,protein=userprotein[0],subprotein=userprotein[1],status=status,amount=price,currency="NGN",tx_ref=tx_ref,content_type=soup_content,object_id=pk)
            elif status == "failed" and soup_product is not None:
                user_transactions = Transactions.objects.create(user=request.user,boxsize=actual_size,protein=userprotein[0],subprotein=userprotein[1],status=status,amount=price,currency="NGN",tx_ref=tx_ref,content_type=soup_content,object_id=pk)
        except Soup.DoesNotExist:
            pass

        try:
            cart = Cart.objects.get(uid=slug)
            cartitems = CartItemsFood.objects.filter(cart=cart)
            cart_content = cartitems_food
            
            if status == "completed" and cart is not None:     
                cart.is_paid = True
                cart.save()
                user_transactions = Transactions.objects.create(user=request.user,cart=list(cartitems.values()),protein=userprotein[0],subprotein=userprotein[1],status=status,amount=price,currency="NGN",tx_ref=tx_ref,content_type=cart_content,object_id=pk)
                cartitems_list = [list(cartitems),status,price]
                new_cartitems = request.session.get('caritems',cartitems_list)
                cart.delete()
            elif status == "failed" and cart is not None:     
                user_transactions = Transactions.objects.create(user=request.user,protein=userprotein[0],subprotein=userprotein[1],status=status,amount=price,currency="NGN",tx_ref=tx_ref,content_type=cart_content,object_id=pk)
                new_cartitems = [cartitems,status,price]
        except Cart.DoesNotExist:
            pass 
        except:
            pass 

    return render(request,'payments/thankyou.html',{
        'food_product':food_product,
        'soup_product':soup_product,
        'cart':new_cartitems,
        'actual_price':actual_price,
        'actual_size':actual_size,
        'food':food_model,
        'soup':soup_model,
        'protein':userprotein[0],
        'subprotein':userprotein[1],
        'status':status,
        })

def transactions(request):

    def user_transactions(transaction):
        list_item = []
        for item in transaction:
            list_item.append(item)
        new = []
        for item in list_item:
            if item.content_type == food_model:
                new.append(item)
            elif item.content_type == soup_model:
                new.append(item)
            else:
                box = []
                amount = item.amount
                status = item.status
                def takes_item(item):
                    for item in item.cart:#Gets all the json items in each cart to iterate over it
                        pk = list(item.values())#Turns each cart item to a list to be able to get the primary key of the object item
                        boxsize = pk[4]#4 is for box size 
                        protein = pk[5]#5 is for protein
                        subprotein = pk[6]#6 is for subprotein
                        quantity = pk[3]#3 is for item quantity
                        try:
                            food_box = Food.objects.get(pk=pk[7])
                        except Food.DoesNotExist:
                            pass
                        try:
                            food_box = Soup.objects.get(pk=pk[7])
                        except Soup.DoesNotExist:
                            pass
                        items = [boxsize,protein,subprotein,food_box,quantity]
                        box.append(items)
                    return box
                all_new = [amount,status,takes_item(item)]
                new.append(all_new)
        return new 
            
    new = Transactions.objects.filter(user=request.user)
    return render(request,'payments/transactions.html',{
        'transactions':user_transactions(new),
        'food_model':food_model,
        'soup_model':soup_model,
        'cart_model':cartitems_food,
        'food':food.model,
        'soup':soup.model,
    })

def payment(request, price, slug):
    email = ""
    username = ""
    mobile = ""
    phone_no = ""
    address = ""
    userprotein = ""
    pk = ""

    try:
        if request.user.is_authenticated:
            address = UserAddress.objects.get(user=request.user)
            username = address.user.username
            email = address.user.email
            mobile = Mobile.objects.get(user=request.user)
            phone_no = mobile.phone_no
            userprotein = request.session.get(str(request.user), ["beef", "fried beef"])

            try:
                food_pk = food.get(slug=slug)
                pk = food_pk.pk
            except Food.DoesNotExist:
                pass
            try:
                soup_pk = soup.get(slug=slug)
                pk = soup_pk.pk
            except Soup.DoesNotExist:
                    pass

            if request.method == "POST":
                payment_method = request.POST.get("paymentMethod")
                if payment_method == "flutterwave":
                    return redirect(reverse('payments:flutterwave', kwargs={
                        'username': username,
                        'email': email,
                        'phone_no': phone_no,
                        'price': price,
                        'pk': pk,
                        'slug':slug,
                    }))
                elif payment_method == "paystack":
                    messages.info(request, "Please, kindly make use of Flutterwave payment gateway. We are currently integrating Paystack.")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.info(request, "Please, kindly make use of Flutterwave payment gateway. We are currently integrating Interswitch.")
                    return redirect(request.META.get('HTTP_REFERER'))
        else:
            address = "Anonymousstreet.com"
            username = "Anonymous-User"
            email = "Anonymoususer@gmail.com"
            phone_no = "081-AnonymousUser"
            userprotein = request.session['userprotein'] = ["beef", "fried beef"]
            
    except Mobile.DoesNotExist:
        messages.error(request, "Please, complete Account Information before proceeding")
        return redirect('authentication:account_info')
    except TypeError:
        pass
    
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
        'address':address,
        'userprotein':userprotein,
        'pk':pk,
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



def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data['id']
        product = soup.get(pk=product_id)   
        id = product.pk
        product_price = data['price']
    
    
        if request.user.is_authenticated:
            protein = request.session.get(str(request.user), ["beef", "fried beef"])
            cart, created = Cart.objects.get_or_create(user=request.user,is_paid=False)
            
            cart_user = Cart.objects.get(user=request.user)
            content = ContentType.objects.get_for_model(product)
            cartitems, created = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,protein=protein[0],subprotein=protein[1],object_id=id,food_category=product_price)
        
            cartitems.quantity += 1
            cartitems.save()   
            num_of_items = cart.total_quantity()
        else:
            try:
                protein = request.session['userprotein']
                cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                content = ContentType.objects.get_for_model(product)
                cartitems, created = CartItemsFood.objects.get_or_create(cart=cart,content_type=content,protein=protein[0],subprotein=protein[1],object_id=id,food_category=product_price)
                
                cartitems.quantity += 1
                cartitems.save()
                num_of_items = cart.total_quantity()
            except:
                request.session['cart_users'] = str(uuid.uuid4())
                cart = Cart.objects.create(session_id=request.session['cart_users'],is_paid=False)
                cart_user = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                content = ContentType.objects.get(model="soup")
                cartitems, created = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,protein=protein[0],subprotein=protein[1],object_id=id,food_category=product_price)
                
                cartitems.quantity += 1
                cartitems.save()
                num_of_items = cart_user.total_quantity()

    except:
        pass
    return JsonResponse(num_of_items,safe=False)

    