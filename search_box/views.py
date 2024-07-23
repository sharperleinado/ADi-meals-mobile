from django.shortcuts import render
from food_app.models import Food,Soup
from cart.models import Cart,CartItemsFood
import json
from django.contrib.contenttypes.models import ContentType
from django.http.response import JsonResponse
import uuid

# Create your views here.

food = Food.objects.all().order_by('food_item')

def search_box(request):
    search_box = ""
    food_box = ""
    soup_box = ""
    search_list = ""
    
    try:
        if request.method == "POST":
            search_box = request.POST.get("search").strip()
            food_box = Food.objects.filter(food_item__contains = search_box).all()
            soup_box = Soup.objects.filter(soup_item__contains = search_box).all()
            search_list = [search_box,food_box,soup_box]
    except:
        pass

    return render(request,'search_box/search_kunkky.html',{'searched':search_box,'food':food_box,'soup':soup_box,
    'search_list':search_list})
    

#Food_search renders all the food and soup search on a different template and accepts a slug request when sent from the user
#which filters the provided slug in the model and display the object model searched by the user to the user.
def food_result(request,slug):
    my_food_box = ""
    my_soup_box = ""
    if request.user.is_authenticated:
        userprotein = request.session.get(str(request.user), ["beef", "fried beef"])
    else:
        userprotein = request.session['userprotein'] = ["beef", "fried beef"]

    def my_foodbox():
        my_food_box = ""
        try:
            my_food_box = Food.objects.get(slug=slug)
        except Food.DoesNotExist:
            pass
        return my_food_box
    
    def my_soupbox():
        my_soup_box = ""
        try:
            my_soup_box = Soup.objects.get(slug=slug)
        except Soup.DoesNotExist:
            pass
        return my_soup_box

    return render(request,'search_box/food_search_kunkky.html',{
        'item':my_foodbox(),
        'item2':my_soupbox(),
        'userprotein':userprotein,
        }) 


def add_to_cart(request):

    data = json.loads(request.body)
    product_id = data['id']
    product = food.get(pk=product_id)
    id = product.pk
    num_of_items = ""
    
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


