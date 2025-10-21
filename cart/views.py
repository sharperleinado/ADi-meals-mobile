from django.shortcuts import render,redirect
from django.contrib import messages
from .models import CartItemsFood,Cart
from django.http import JsonResponse
from django.http.response import JsonResponse
from django.contrib.contenttypes.models import ContentType
import json
from authentication.models import User

# Create your views here.


food_model = ContentType.objects.get(model="food")
soup_model = ContentType.objects.get(model="soup")


def returns_item(item,food_category):
    if item.content_type == food_model:
        total_price = item.total_price(food_category)
        new_list = [item,total_price]
    elif item.content_type == soup_model and item.food_category == food_category:
        total_price = item.total_price(food_category)
        new_list = [item,total_price]
    return new_list



def cart_items(request):
    new_cartitems = []
    cart = ""
    protein = ""

    request.session['protein'] = {'beef':['fried beef','boiled beef'],
                                        'chicken':['fried chicken','boiled chicken'],
                                        'fish':['fried fish','boiled fish'],
                                        'goat':['fried goat','boiled goat'],
                                        }
    
    protein = request.session['protein'].items()

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
        cartitems = cart.cartitems.all()

        if len(cartitems) == 0:
            messages.info(request,"Add to cart to view items!")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            for item in cartitems:
                new_cartitems.append(returns_item(item,item.food_category))
            new_cartitems = new_cartitems
            
            if request.method == "POST":
                protein_select = request.POST.get("protein")
                subprotein_select = request.POST.get("subprotein")
                item = request.POST.get("item_id")
                food_category = request.POST.get("food_category")

                cartitemfood = CartItemsFood.objects.get(cart=cart,object_id=item,food_category=food_category)
                print(cartitemfood.content_object)
                def return_protein(item):#here protein return was defined to return the particular item of the protein change.
                    if item.content_type == food_model:
                       protein = [item.content_object.food_item,cartitemfood.total_price(item.food_category)]
                    elif item.content_type == soup_model:
                        protein [item.content_object.soup_item,cartitemfood.total_price(item.food_category)]
                    return protein
            
                if cartitemfood.protein is not protein_select and cartitemfood.subprotein is not subprotein_select:
                    cartitemfood.protein = protein_select
                    cartitemfood.subprotein = subprotein_select
                    cartitemfood.save()
                else:
                    messages.info(request,"Item and Protein already exist in cart!")
                    return redirect(request.META.get('HTTP_REFERER'))
                
                #messages.info(request, f"You have successfully changed protein")
                messages.info(request, f"You have successfully changed protein to {protein_select.capitalize()} | {subprotein_select.capitalize()} for {return_protein(cartitemfood)[0].capitalize()} | Total = {return_protein(cartitemfood)[1]}")
                return redirect(request.META.get('HTTP_REFERER'))
    except Cart.DoesNotExist:
        messages.info(request,"Add to cart to view items!")
        return redirect(request.META.get('HTTP_REFERER'))
    except KeyError:
        messages.info(request,"Add to cart to view items!")
        return redirect(request.META.get('HTTP_REFERER'))
    
    return render(request,'cart/cartitems_kunkky.html',{
        'food':food_model,
        'soup':soup_model,
        'new':new_cartitems[::-1],
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
        print(name)
        form = data['form']
        
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItemsFood.objects.filter(cart=cart)
            total_quantities = cart.total_quantity()

            if name == "add-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity += 1
                if item.quantity <= 10:
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
                total_quantities = total_quantities - 1
                list_item = [cartitem_price,new_quantity,total_quantities,cart.total_price(),len(cart_items)]
            
        else:
            cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
            cart_items = CartItemsFood.objects.filter(cart=cart)
            total_quantities = cart.total_quantity() 
            
            if name == "add-item":
                item = cart_items.get(object_id=object_id,food_category=form)
                item.quantity += 1
                if item.quantity <= 10:
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
                total_quantities = total_quantities - item.quantity
                list_item = [cartitem_price,new_quantity,total_quantities,cart.total_price(),len(cart_items),name]
            
    except:
        pass

    return JsonResponse(list_item, safe=False)


def clear_all(request):
    data = json.loads(request.body)
    cart = data['okay_value']
    print(cart)

    if request.user.is_authenticated:
        cart_object = Cart.objects.get(uid=cart)
        cart_object.delete()
    else:
        cart_object = Cart.objects.get(uid=cart)
        cart_object.delete()
    
    return JsonResponse(data,safe=False)

