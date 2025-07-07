from django.shortcuts import render,redirect
from django.http.response import JsonResponse
import json
from cart.models import Cart,CartItemsFood
from django.contrib.contenttypes.models import ContentType
from authentication.models import Mobile,User
import math
import random
from food_app.models import Food,Soup
import requests
from food_app.views import food,soup
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
from django.core.mail import send_mail
from address.views import state_and_lga
from cart.views import returns_item
load_dotenv()

# Create your views here.

food_model = ContentType.objects.get(model="food")
soup_model = ContentType.objects.get(model="soup")
cart_model = ContentType.objects.get(model="cart")
cartitems_food = ContentType.objects.get(model="cartitemsfood")



def tx_ref():
    tx_ref = ''+str(math.floor(1000000 + random.random()*9000000))
    return  tx_ref


def paystack(request, username, email, phone_no, price, pk, slug, delivery):
    url = "https://api.paystack.co/transaction/initialize"
    authorization = {
        "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json"
    }
    data = {
        "amount": int(price * 100),
        "currency": "NGN",
        "email":email,
        "reference": tx_ref(),
        "callback_url": f"http://adimeals.com/payments/verify_payment/{price}/{pk}/{slug}/{delivery}",
        "metadata": {
        "custom_fields": [
            {
            "display_name": "ADi meals",
            "variable_name": "ADi meals",
            "value": "ADi"
            },
            {
            "display_name": "Paystack",
            "variable_name": "Paystack",
            "value": "API call"
            }
        ]
        },
        "customer": {
            "id": pk,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": email,
            "customer_code": "CUS_hns72vhhtos0f0k",
            "phone": phone_no,
            "risk_action": "default"
            },
    }

    try:
        response = requests.post(url, headers=authorization, json=data)

        response.raise_for_status()  # Raise an error for bad status codes

        json_response = response.json()
        generated_link = json_response['data']
        print(json_response['status'])
        return redirect(generated_link['authorization_url'])
        
    except requests.exceptions.RequestException as err:
        error_message = f"Error: {err}"
        print(error_message)
        return JsonResponse({"error": error_message}, status=500, safe=False)


def flutterwave(request,username,email,phone_no,price,pk,slug,delivery):
    
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {os.getenv('FLUTTERWAVE_SECRET_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "tx_ref": tx_ref(),
        "amount": float(price),
        "currency": "NGN",
        "redirect_url": f"http://adimeals.com/payments/verify_payment/{price}/{pk}/{slug}/{delivery}",#"http://localhost:8000/payments/verify_payment",
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
            "title": "ADi meals",
            "logo": "https://i.imgur.com/MnUGFHi.jpeg"
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



def verify_payment(request,price,pk,slug,delivery):
    new_cartitems = ""
    food_item = ""
    
    userprotein = request.session.get(str(request.user), ["beef", "fried beef"])

    user = User.objects.get(username=request.user.username)

    address = UserAddress.objects.get(user=user)

    mobile = Mobile.objects.get(user=user)

    if request.method == "GET":
        #status = request.GET.get("status")
        #tx_ref = request.GET.get("tx_ref")
        #trxref = request.GET.get("trxref")
        def reference():#To get the reference number from the frontend
            tx_ref = request.GET.get("tx_ref")
            trxref = request.GET.get("trxref")
            if tx_ref is not None:
                return tx_ref
            else:
                return trxref 
        
        def verify_status(ref):#Verifies payment status if it is from Paystack
            # Step 1: Call the Paystack API to verify the payment status
            try:
                # Send a GET request to Paystack to verify the transaction
                url = f"https://api.paystack.co/transaction/verify/{reference()}"
                headers = {
                    "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",  # Your Paystack secret key
                    "Cache-Control": "no-cache",
                    "Content-Type": "application/json"
                }

                # Send the GET request
                response = requests.get(url, headers=headers)

                # Raise exception if the response status is not OK
                response.raise_for_status()

                # Parse the JSON response
                json_response = response.json()
                print(json_response.get('status'))
                print(json_response)

                # Step 2: Check if the payment was successful
                if json_response['message'] == 'Verification successful' and json_response['data']['status'] == 'success':
                    status = "successful"
                    # Proceed to save or update the transaction record
                    # You can handle saving the transaction data in your database here
                else:
                    status = "failed"
                    
            except requests.exceptions.RequestException as err:
                status = "failed"
                print(f"Error verifying transaction: {err}")
                return JsonResponse({"error": f"Error verifying transaction: {err}"}, status=500)
            
            return status
        
        
        def status():#To get the status of the transaction from the frontend
            status = request.GET.get("status")
            if status is not None:
                return status
            else:
                return verify_status(reference())
            
        try:
            food_item = food.get(slug=slug,pk=pk)
            food_content = ContentType.objects.get_for_model(food_item)
            if status() == "successful" or status() == "completed" or status() == "success" and food_item is not None:
                user_transactions = Transactions.objects.get_or_create(user=request.user,boxsize="mini",protein=userprotein[0],subprotein=userprotein[1],status=status(),amount=price,currency="NGN",tx_ref=reference(),content_type=food_content,object_id=pk,delivery=delivery,address=[address.state,address.division,address.lga,address.lcda,address.street_name],mobile=[str(mobile.phone_no)])
            elif status() == "failed" and food_item is not None:
                user_transactions = Transactions.objects.get_or_create(user=request.user,boxsize="mini",protein=userprotein[0],subprotein=userprotein[1],status=status(),amount=price,currency="NGN",tx_ref=reference(),content_type=food_content,object_id=pk,delivery=delivery,address=[address.state,address.division,address.lga,address.lcda,address.street_name],mobile=[str(mobile.phone_no)])
        except Food.DoesNotExist:
            pass
    
        try:
            food_item = soup.get(slug=slug)
            soup_content = ContentType.objects.get_for_model(food_item)
            def actual_size():
                if food_item.mini_box_price == price:
                    actual_size = food_item.mini_box_name
                elif food_item.medium_box_price == price:
                    actual_size = food_item.medium_box_name
                else:
                    actual_size = food_item.mega_box_name
                return actual_size
        


            if status() == "successful" or status() == "completed" or status() == "success" and food_item is not None:
                user_transactions = Transactions.objects.get_or_create(user=request.user,boxsize=actual_size(),protein=userprotein[0],subprotein=userprotein[1],status=status(),amount=price,currency="NGN",tx_ref=reference(),content_type=soup_content,object_id=pk,delivery=delivery,address=[address.state,address.division,address.lga,address.lcda,address.street_name],mobile=[str(mobile.phone_no)])
            elif status() == "failed" and food_item is not None:
                user_transactions = Transactions.objects.get_or_create(user=request.user,boxsize=actual_size(),protein=userprotein[0],subprotein=userprotein[1],status=status(),amount=price,currency="NGN",tx_ref=reference(),content_type=soup_content,object_id=pk,delivery=delivery,address=[address.state,address.division,address.lga,address.lcda,address.street_name],mobile=[str(mobile.phone_no)])
        except Soup.DoesNotExist:
            pass

        try:
            cart = Cart.objects.get(uid=slug)
            cartitems = CartItemsFood.objects.filter(cart=cart)
            cart_content = cartitems_food
            
            if status() == "successful" or status() == "completed" or status() == "success" and cart is not None:     
                cart.is_paid = True
                cart.save()
                user_transactions = Transactions.objects.get_or_create(user=request.user,cart=list(cartitems.values()),protein=userprotein[0],subprotein=userprotein[1],status=status(),amount=price,currency="NGN",tx_ref=reference(),content_type=cart_content,object_id=pk,delivery=delivery,cart_item_price=str(cart.total_price()),address=[address.state,address.division,address.lga,address.lcda,address.street_name],mobile=[str(mobile.phone_no)])
                cartitems_list = [list(cartitems),status(),price]
                food_item = request.session.get('caritems',cartitems_list)
                print(food_item)
                cart.delete()
            elif status() == "failed" and cart is not None:     
                user_transactions = Transactions.objects.get_or_create(user=request.user,cart=list(cartitems.values()),protein=userprotein[0],subprotein=userprotein[1],status=status(),amount=price,currency="NGN",tx_ref=reference(),content_type=cart_content,object_id=pk,delivery=delivery,cart_item_price=str(cart.total_price()),address=[address.state,address.division,address.lga,address.lcda,address.street_name],mobile=[str(mobile.phone_no)])
                food_item = [cartitems,status(),price]
            elif status() == "cancelled" and cart is not None:
                food_item = [cartitems,status(),price]
        except:
            pass

    return render(request,'payments/thankyou.html',{
        'food_product':food_item,
        'cart':new_cartitems,
        'price':price,
        'soup_price':price - delivery,
        'food':food_model,
        'soup':soup_model,
        'protein':userprotein[0],
        'subprotein':userprotein[1],
        'status':status(),
        })



def all_transactions(request):
    #subject = "Email Testing"
    #essage = "Let's try to send an email"
    #from_email = "adimeals@gmail.com"
    #recipient_list = ["dannyhance7420@gmail.com"]
    #send_mail(subject,message,from_email,recipient_list,fail_silently=False)

    def superuser_transactions(all_transaction):
        selected_user_transaction = []
        for item in all_transaction:
            if item.content_type == food_model:
                user_details = [item]
                selected_user_transaction.append(user_details)
            elif item.content_type == soup_model:
                user_details = [item]
                selected_user_transaction.append(user_details)
            else:
                box = []
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
                        box.append(items)#Puts all item.cart in a list 
                    return box
                user_details = [item,takes_item(item)]
                selected_user_transaction.append(user_details)
        return selected_user_transaction

    return render(request,'payments/all_transactions.html',{
        'all_transactions':superuser_transactions(Transactions.objects.all().order_by('-datetime','-time')),
        'food_model':food_model,
        'soup_model':soup_model,
    })



def transactions(request):
    
    try:
        Transactions.objects.get(user=request.user)
    except Transactions.DoesNotExist:
        messages.error(request, "You have ZERO transactions!")
        return redirect('profile')
    except Transactions.MultipleObjectsReturned:
        pass
    
    def user_transactions(transaction):
        new = []
        for item in transaction:
            if item.content_type == food_model:
                new.append(item)
            elif item.content_type == soup_model:
                new.append(item)
            else:
                box = []
                amount = item.amount
                status = item.status
                date_time = item.datetime
                time = item.time
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
                all_new = [amount,status,takes_item(item),date_time,time]
                new.append(all_new)
        return new 
            
    new = Transactions.objects.filter(user=request.user).order_by('-datetime','-time')
    return render(request,'payments/transactions.html',{
        'transactions':user_transactions(new),
        'food_model':food_model,
        'soup_model':soup_model,
        'cart_model':cartitems_food,
        'food':food.model,
        'soup':soup.model,
    })




def delivery_price(address_user,lcda):
    for item in lcda:
        if item[:][0] == address_user.lcda:
            break
    
    return item


def cart_delivery_price(address_user,lcda,cart):
    for item in lcda: 
        if item[:][0] == address_user.lcda:
            new_price = 50 * cart.total_quantity()
            break
    new_item = sum([item[1],new_price])

    return new_item




def payment(request, price, slug,):
    new_cartitems = []
    email = ""
    username = ""
    mobile = ""
    phone_no = ""
    address = ""
    userprotein = ""
    pk = ""
    cart = ""
    cartitems = ""

    lcda = ""
    lga = ""
    division = ""
    delivery = 0
    total = 0
    cart_deliveryprice = 0
    cart_total = 0



    request.session['protein'] = {'beef':['fried beef','boiled beef'],
                                    'chicken':['fried chicken','boiled chicken'],
                                    'fish':['fried fish','boiled fish'],
                                    'goat':['fried goat meat','boiled goat meat'],
                                    }
    protein = request.session['protein'].items()

    request.session['price-slug'] = [price,slug]

    try:
        if request.user.is_authenticated:
            address = UserAddress.objects.get(user=request.user)
            username = address.user.username
            email = address.user.email
            mobile = Mobile.objects.get(user=request.user)
            phone_no = mobile.phone_no
            userprotein = request.session.get(str(request.user), ["beef", "fried beef"])

            division = state_and_lga.get(address.state)
            lga = division.get(address.division)
            lcda = lga.get(address.lga)

            
            try:
                cart = Cart.objects.get(user=request.user)
                cartitems = cart.cartitems.all()
                pk = cart.pk
                
                delivery = float(cart_delivery_price(address,lcda,cart))
                total = float(sum([cart_delivery_price(address,lcda,cart),cart.total_price()]))
            except Cart.DoesNotExist:
                pass

            try:
                food_pk = food.get(slug=slug)
                pk = food_pk.pk
                price = food_pk.food_price
                delivery = float(delivery_price(address,lcda)[1])
                total = float(sum([delivery_price(address,lcda)[1],price]))
            except Food.DoesNotExist:
                pass

            try:
                soup_pk = soup.get(slug=slug)
                pk = soup_pk.pk
                price = price 
                delivery = float(delivery_price(address,lcda)[1])
                total = float(sum([delivery_price(address,lcda)[1],price]))
            except Soup.DoesNotExist:
                    pass
            

            if request.method == "POST":
                if 'protein' in request.POST:
                    protein_select = request.POST.get("protein")
                    subprotein_select = request.POST.get("subprotein")
                    print(protein_select)
                    print(subprotein_select)
                    if request.user.is_authenticated:
                        request.session[str(request.user)] = [protein_select, subprotein_select]
                        messages.info(request, f"You have successfully changed protein to {protein_select.capitalize()} | {subprotein_select.capitalize()}")
                        print(request.session[str(request.user)])
                        return redirect(request.META.get('HTTP_REFERER'))
            
                elif 'paymentMethod' in request.POST:
                    payment_method = request.POST.get("paymentMethod")
                    if payment_method == "flutterwave":
                        return redirect(reverse('payments:flutterwave', kwargs={
                            'username': username,
                            'email': email,
                            'phone_no': phone_no,
                            'price': int(total),#int(price),
                            'pk': pk,
                            'slug': slug,
                            'delivery':delivery,
                        }))
                    elif payment_method == "paystack":
                        return redirect(reverse('payments:paystack', kwargs={
                            'username': username,
                            'email': email,
                            'phone_no': phone_no,
                            'price': int(total),#int(price),
                            'pk': pk,
                            'slug': slug,
                            'delivery':delivery,
                        }))
                    else:
                        messages.info(request, "Please, kindly make use of Flutterwave or Paystack payment gateway. We are currently integrating Interswitch.")
                        return redirect(request.META.get('HTTP_REFERER'))
        else:
            address = "Anonymousstreet.com"
            username = "Anonymous-User"
            email = "Anonymoususer@gmail.com"
            phone_no = "081-AnonymousUser"
            userprotein = request.session['userprotein'] = ["beef", "fried beef"]

            try:
                cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                cartitems = cart.cartitems.all()
            except Cart.DoesNotExist:
                pass
            except KeyError:
                pass

        for item in cartitems:
            new_cartitems.append(returns_item(item,item.food_category))
        new_cartitems = new_cartitems  
            
    except Mobile.DoesNotExist:
        messages.error(request, "Please, complete Account Information before proceeding!")
        return redirect('authentication:account_info')
    except TypeError:
        pass
    except UserAddress.DoesNotExist:
        messages.error(request, "Please, register address before proceeding!")
        return redirect('address:register_address')

    
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
        'protein':protein,
        'cart':cart,
        'food':food_model,
        'soup':soup_model,
        'new':new_cartitems,
        'delivery_price':delivery,
        'total':total,
    })




def change_protein(request):
    if request.method == "POST":
        data = json.loads(request.body)
        protein_value = data.get('id')
        subproteins = request.session['protein'].get(protein_value, [])
        print(subproteins)
        return JsonResponse(subproteins, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


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
            if cartitems.quantity <= 10:
                cartitems.save()   
            num_of_items = [cart.total_quantity(),cartitems.quantity]
        else:
            try:
                protein = request.session['userprotein']
                cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                content = ContentType.objects.get_for_model(product)
                cartitems, created = CartItemsFood.objects.get_or_create(cart=cart,content_type=content,protein=protein[0],subprotein=protein[1],object_id=id,food_category=product_price)
                
                cartitems.quantity += 1
                if cartitems.quantity <= 10:
                    cartitems.save()
                num_of_items = [cart.total_quantity(),cartitems.quantity]
            except:
                request.session['cart_users'] = str(uuid.uuid4())
                cart = Cart.objects.create(session_id=request.session['cart_users'],is_paid=False)
                cart_user = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                content = ContentType.objects.get(model="soup")
                cartitems, created = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,protein=protein[0],subprotein=protein[1],object_id=id,food_category=product_price)
                
                cartitems.quantity += 1
                if cartitems.quantity <= 10:
                    cartitems.save()
                num_of_items = [cart_user.total_quantity(),cartitems.quantity]

    except:
        pass
    return JsonResponse(num_of_items,safe=False)



def edit_account(request,price,slug):
    #This is a view to edit a user's account information

    #What I did here is, I first of all listed out all the details of the user currently logged in 
    #Then I got all the user inputs from the "Edit info template"
    #After which I got the User object, then inserted each new input from edit info template.

    #Here I added a Phone number form to this view to update phone number
    form = ""
    try:
        model = Mobile.objects.get(user=request.user)

        if request.method == "POST":
            form = request.POST.get("update_mobile_no").strip()
            if len(form) == 0:
                messages.info(request, "PHONE NUMBER unchanged!")
                return redirect(reverse('payments:payment', args=[price,slug]))
            elif len(form) > 14 or len(form) < 14:
                messages.error(request, "PHONE NUMBER must be 14 digits!")
                return redirect(reverse('payments:edit_account', args=[price,slug]))
            elif form == model.phone_no:
                messages.error(request, "Phone number already in use by you. Change number to proceed")
                return redirect(reverse('payments:payment', args=[price,slug]))
            else:
                #request.session['update_mobile'] = form
                #messages.success(request, "Please, input the one time password sent to " + form)
                #update_mobile_send_otp(request)
                #return redirect('authentication:otp') 

                model = Mobile.objects.get(user=request.user)
                model.phone_no = form
                model.save()
                messages.success(request, "You have successfully updated your Phone Number!")
                return redirect(reverse('payments:payment', args=[price,slug]))
    
    except AttributeError:
        pass
    except Mobile.DoesNotExist:
        messages.info(request, "Please, complete account information before editing account")
        return redirect('address:register_address')
    except ConnectionError:
        messages.error(request, "Please, be sure to check your internet connection!\nIf you did not receive your otp, redirect back to the previous page, and ensure your internet is on.")
        return redirect(reverse('payments:payment', args=[price,slug]))
    

    try:
        user_uname = request.user.username
        user_fname = request.user.first_name
        user_lname = request.user.last_name
        user_email = request.user.email
    
        user = User.objects.get(username=user_uname)
    
        if request.method == "POST":
            uname = request.POST.get("username").strip()       
            fname = request.POST.get("fname").strip()
            lname = request.POST.get("lname").strip()
            email = request.POST.get("email").strip()
        
            uname = uname.lower()
            email = email.lower()

            if User.objects.filter(username=uname):
                messages.error(request, "Username has been taken!\nPlease, try another username.")
                return redirect(reverse('payments:edit_account', args=[price,slug]))
            elif User.objects.filter(email=email):
                messages.error(request, "Email has been taken!\nPlease, try another Email.")
                return redirect(reverse('payments:edit_account', args=[price,slug]))

            if uname == "":
                uname = user_uname
            else:
                user.username = uname
                user.save()
            if fname == "":
                fname = user_fname 
            else:
                user.first_name = fname 
                user.save()
            if lname == "":
                lname = user_lname
            else:
                user.last_name = lname
                user.save()
            if email == "":
                email = user_email
            else:
                user.email = email
                user.save()
            messages.success(request, "You have successfully updated your account details!")
            return redirect(reverse('payments:payment', args=[price,slug]))
    except AttributeError:
        pass
    
    
    
    try:
        user = UserAddress.objects.get(user=request.user)
        if request.method == "POST":
            state = request.POST.get("state")
            division = request.POST.get("division")
            lga = request.POST.get("lga")
            lcda = request.POST.get("lcda")
            street_name = request.POST.get("street_name")
            
            user.state = state
            user.division = division
            user.lga = lga
            user.lcda = lcda
            user.street_name = street_name
            user.save()
            messages.success(request, "You have successfully updated address.")
            return redirect(reverse('payments:payment', args=[price,slug]))
    except:
        pass
        
    return render(request,'authentication/edit_account.html',{'state_lga':state_and_lga.items()})

