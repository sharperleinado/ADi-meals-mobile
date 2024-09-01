from django.shortcuts import render,redirect
from django.contrib import messages
from .models import CartItemsFood,Cart
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.http.response import JsonResponse
import json
from authentication.models import Mobile
from payments.views import tx_ref
from address.models import UserAddress
from django.template import *
from django.urls import reverse
from payments.models import Transactions

# Create your views here.


food_model = ContentType.objects.get(model="food")
soup_model = ContentType.objects.get(model="soup")

def returns_item(items,food_category):
        new_items = []
        for item in items:
            if item.content_type == food_model:
                total_price = item.total_price(item.food_category)
                new_list = [item,total_price]
                new_items.append(new_list)
            elif item.content_type == soup_model and item.food_category == item.food_category:
                total_price = item.total_price(item.food_category)
                new_list = [item,total_price]
                new_items.append(new_list)
        return new_items

def cart_items(request):
    new_cartitems = ""
    cart = ""
    protein = ""

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
        cartitems = cart.cartitems.all()
        if len(cartitems) == 0:
            messages.info(request,"Add items to cart to view items!")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            new_cartitems = returns_item(cartitems,"mini_box")

        request.session['protein'] = {'beef':['fried beef','boiled beef'],
                                    'chicken':['fried chicken','boiled chicken'],
                                    'fish':['fried fish','boiled fish'],
                                    'goat':['fried goat','boiled goat'],
                                    }
        protein = request.session['protein'].items()

        if request.method == "POST":
            protein_select = request.POST.get("protein")
            subprotein_select = request.POST.get("subprotein")
            item = request.POST.get("item_id")
            cartitemfood = CartItemsFood.objects.get(pk=item)
            if cartitemfood.protein is not protein_select and cartitemfood.subprotein is not subprotein_select:
                cartitemfood.protein = protein_select
                cartitemfood.subprotein = subprotein_select
                cartitemfood.save()
            else:
                pass
            messages.info(request,"You have successfully changed protein")
            return redirect(request.META.get('HTTP_REFERER'))
                
    except Mobile.DoesNotExist:
        messages.info(request,"Add Mobile no before viewing cart!")
        return redirect(request.META.get('HTTP_REFERER'))
    except Cart.DoesNotExist:
        messages.info(request,"Add items to cart to view items!")
        return redirect(request.META.get('HTTP_REFERER'))
    except KeyError:
        messages.info(request,"Add items to cart to view items!")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.info(request,"Add items to cart to view items!")
        return redirect(request.META.get('HTTP_REFERER'))
    
    return render(request,'cart/new.html',{
        'food':food_model,
        'soup':soup_model,
        'new':new_cartitems,
        'protein':protein,
        })

def change_cart_protein(request):
    if request.method == "POST":
        data = json.loads(request.body)
        protein_value = data.get('id')
        subproteins = request.session['protein'].get(protein_value, [])
        print(subproteins)

        return JsonResponse(subproteins, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_buttons(request):
    try:
        list_item = ""
        data = json.loads(request.body)
        object_id = data['id']
        name = data['btn_name']
        form = data['form']
        
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItemsFood.objects.filter(cart=cart)
            total_quantities = cart.total_quantity()

            if name == "add-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity += 1
                item.save()
                cartitem_price = item.total_price(item.food_category)
                new_quantity = item.quantity
                total_quantities = total_quantities + 1
                list_item = [cartitem_price,new_quantity,total_quantities,cart.total_price(),len(cart_items)]
            elif name == "subtract-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity -= 1
                item.save()
                cartitem_price = item.total_price(item.food_category)
                new_quantity = item.quantity
                if item.quantity < 1:
                    item.delete()
                    cartitem_price = 0
                    new_quantity = 0
                total_quantities = total_quantities - 1
                list_item = [cartitem_price,new_quantity,total_quantities,cart.total_price(),len(cart_items)]  
            else:
                item = cart_items.get(object_id=object_id,food_category=form)
                item.delete()
                cartitem_price = 0
                new_quantity = 0
                total_quantities -= item.quantity
                list_item = [cartitem_price,new_quantity,total_quantities,0,len(cart_items)]
            
        else:
            cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
            cart_items = CartItemsFood.objects.filter(cart=cart)
            total_quantities = cart.total_quantity() 
            
            if name == "add-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity += 1
                item.save()
                cartitem_price = item.total_price(item.food_category)
                new_quantity = item.quantity
                total_quantities = total_quantities + 1
                list_item = [cartitem_price,new_quantity,total_quantities,cart.total_price(),len(cart_items)]
            elif name == "subtract-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity -= 1
                item.save()
                cartitem_price = item.total_price(item.food_category)
                new_quantity = item.quantity
                if item.quantity < 1:
                    item.delete()
                    cartitem_price = 0
                    new_quantity = 0
                total_quantities = total_quantities - 1
                list_item = [cartitem_price,new_quantity,total_quantities,cart.total_price(),len(cart_items)]  
            else:
                item = cart_items.get(object_id=object_id,food_category=form)
                item.delete()
                cartitem_price = 0
                new_quantity = 0
                total_quantities -= item.quantity
                list_item = [cartitem_price,new_quantity,total_quantities,0,len(cart_items)]
            
    except:
        pass

    return JsonResponse(list_item, safe=False)


def clear_all(request):
    data = json.loads(request.body)
    cart = data['okay_value']
    print(cart)

    if request.user.is_authenticated:
        cart_object = Cart.objects.get(user=cart)
        cart_object.delete()
    else:
        cart_object = Cart.objects.get(session_id=cart)
        cart_object.delete()
    
    return JsonResponse(data,safe=False)


def checkout(request):
    address = ""
    cart = ""
    new_cartitems = ""
    cart_pk = ""
    username = ""
    phone_no = ""
    email = ""

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            address = UserAddress.objects.get(user=request.user)
            username = address.user.username
            email = address.user.email
            mobile = Mobile.objects.get(user=request.user)
            phone_no = mobile.phone_no

            new = request.session.get('cartitems')
            del new 
        else:
            cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
            address = "Anonymousstreet.com"
            username = "Anonymous-User"
            email = "Anonymoususer@gmail.com"
            phone_no = "081-AnonymousUser"
        cartitems = cart.cartitems.all()
        new_cartitems = returns_item(cartitems,"mini_box")

        if request.method == "POST":
            payment_method = request.POST["paymentMethod"]
            if payment_method == "flutterwave":
                print(payment_method)
                return redirect(reverse('payments:flutterwave', kwargs={
                    'username': username,
                    'email': address.user.email,
                    'phone_no': phone_no,
                    'price': cart.total_price(),
                    'pk': cart.pk,
                    'slug':cart.uid,
                }))
            elif payment_method == "paystack":
                messages.info(request, "Please, kindly make use of Flutterwave payment gateway. We are currently integrating Paystack.")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.info(request, "Please, kindly make use of Flutterwave payment gateway. We are currently integrating Interswitch.")
                return redirect(request.META.get('HTTP_REFERER'))
            
    except Exception as e:
        pass

    return render(request,'cart/checkout.html',{
        'address':address,
        'username':username,
        'email': email,
        'food':food_model,
        'soup':soup_model,
        'new':new_cartitems,
        'phone_no':phone_no,
        })

