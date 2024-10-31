from django.shortcuts import render
from food_app.models import Food,Soup
from cart.models import Cart,CartItemsFood
from django.http.response import JsonResponse
import json
from django.contrib.contenttypes.models import ContentType
import uuid
from django.contrib import messages
from django.shortcuts import redirect



# Create your views here.

#what food box function does is, first, I used a for loop on the model Food, then listed all the field in the models
#such as: image,food_item,food_price and food slug. put the=m in a list
#and then append them into a list and did the same for all the objects in the model.
food = Food.objects.all().order_by('food_item')
soup = Soup.objects.all().order_by('soup_item')


def food_box(request):

    request.session['protein'] = {'beef':['fried beef','boiled beef'],
                                    'chicken':['fried chicken','boiled chicken'],
                                    'fish':['fried fish','boiled fish'],
                                    'goat':['fried goat','boiled goat'],
                                    }

    protein = request.session['protein'].items()
    anonymousprotein = request.session['userprotein'] = ["beef", "fried beef"]

    if request.method == "POST":
        protein_select = request.POST.get("protein")
        subprotein_select = request.POST.get("subprotein")
        print(protein_select)
        print(subprotein_select)
        if request.user.is_authenticated:
            request.session[str(request.user)] = [protein_select, subprotein_select]
            messages.info(request,"You have successfully changed protein")
            print(request.session[str(request.user)])
            return redirect(request.META.get('HTTP_REFERER'))
    
    userprotein = request.session.get(str(request.user), ["beef", "fried beef"])

    return render(request,'food_app/food_box_kunkky.html',{'food':food,
                                                           'protein':protein,
                                                           'anonymousprotein':anonymousprotein,
                                                           'userprotein':userprotein,
                                                           })


def soup_box(request):
    
    if request.user.is_authenticated:
        userprotein = request.session.get(str(request.user), ["beef", "fried beef"])
    else:
        userprotein = request.session.get('userprotein', ["beef", "fried beef"])
    
    return render(request,'food_app/soup_box_kunkky.html',{'soup':soup,
                                                            'userprotein':userprotein,
                                                            })

#for food box page add to cart
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = food.get(pk=product_id)
    id = product.pk
    num_of_items = ""
    protein = ""
    
    if request.user.is_authenticated:
        protein = request.session.get(str(request.user), ["beef", "fried beef"])
        cart = Cart.objects.get_or_create(user=request.user,is_paid=False)
            
        cart_user = Cart.objects.get(user=request.user)
        content = ContentType.objects.get(model="food")
        cartitems, created = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,protein=protein[0],subprotein=protein[1],object_id=id)

        cartitems.quantity += 1
        cartitems.save()
        num_of_items = cart_user.total_quantity()
    
    else:
        try:
            protein = request.session['userprotein']
            cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
            content = ContentType.objects.get(model="food")
            cartitems, created = CartItemsFood.objects.get_or_create(cart=cart,content_type=content,protein=protein[0],subprotein=protein[1],object_id=id)
            
            cartitems.quantity += 1
            cartitems.save()
            num_of_items = cart.total_quantity()
        except:
            request.session['cart_users'] = str(uuid.uuid4())
            cart = Cart.objects.create(session_id=request.session['cart_users'],is_paid=False)
            cart_user = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
            content = ContentType.objects.get(model="food")
            cartitems, created = CartItemsFood.objects.get_or_create(cart=cart_user,content_type=content,protein=protein[0],subprotein=protein[1],object_id=id)
            
            cartitems.quantity += 1
            cartitems.save()
            num_of_items = cart_user.total_quantity()
    
    return JsonResponse(num_of_items,safe=False)


def change_protein(request):
    if request.method == "POST":
        data = json.loads(request.body)
        protein_value = data.get('id')
        subproteins = request.session['protein'].get(protein_value, [])
        print(subproteins)
        return JsonResponse(subproteins, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)
