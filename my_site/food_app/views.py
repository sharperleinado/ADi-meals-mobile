from django.http import Http404
from django.shortcuts import redirect, render
from food_app.models import Food, Soup
from django.contrib import messages
#from .forms import Price

# Create your views here.


def food_box(request):

    my_food_box = Food.objects.all()

    ewa_aganyin = my_food_box.get(pk=1)
    ewa_item = ewa_aganyin.food_item
    ewa_price = ewa_aganyin.food_price

    poundyam = my_food_box.get(pk=2)
    pound_item = poundyam.food_item
    pound_price = poundyam.food_price

    poundyam_2 = my_food_box.get(pk=3)
    pound2_item = poundyam_2.food_item
    pound2_price = poundyam_2.food_price

    semo = my_food_box.get(pk=4)
    semo_item = semo.food_item
    semo_price = semo.food_price

    semo2 = my_food_box.get(pk=5)
    semo2_item = semo2.food_item
    semo2_price = semo2.food_price

    eba = my_food_box.get(pk=6)
    eba_item = eba.food_item
    eba_price = eba.food_price

    eba2 = my_food_box.get(pk=7)
    eba2_item = eba2.food_item
    eba2_price = eba2.food_price

    ofada = my_food_box.get(pk=8)
    ofada_item = ofada.food_item
    ofada_price = ofada.food_price

    jollof = my_food_box.get(pk=9)
    jollof_item = jollof.food_item
    jollof_price = jollof.food_price

    rice = my_food_box.get(pk=10)
    rice_item = rice.food_item
    rice_price = rice.food_price

    fried_rice = my_food_box.get(pk=11)
    friedrice_item = fried_rice.food_item
    friedrice_price = fried_rice.food_price

    peppersoup = my_food_box.get(pk=12)
    peppersoup_item = peppersoup.food_item
    peppersoup_price = peppersoup.food_price

    food_box = {'food_box1':[ewa_item,ewa_price],'food_box2':[pound_item,pound_price],
    'food_box3':[pound2_item,pound2_price],'food_box4':[semo_item,semo_price],
    'food_box5':[semo2_item,semo2_price],'food_box6':[eba_item,eba_price],
    'food_box7':[eba2_item,eba2_price],'food_box8':[ofada_item,ofada_price],
    'food_box9':[jollof_item,jollof_price],'food_box10':[rice_item,rice_price],
    'food_box11':[friedrice_item,friedrice_price],'food_box12':[peppersoup_item,peppersoup_price],}

    return render(request,'food_app/food_box.html',context=food_box)


def price_in_packs(request):
    total_price1 = ""
    total_price2 = ""
    total_price3 = ""
    total_price4 = ""
    total_price5 = ""
    total_price6 = ""
    total_price7 = ""
    total_price8 = ""
    total_price9 = ""
    total_price10 = ""
    total_price11 = ""
    total_price12 = ""

    price_pack_box1 = ""
    price_pack_box2 = ""
    price_pack_box3 = ""
    price_pack_box4 = ""
    price_pack_box5 = ""
    price_pack_box6 = ""
    price_pack_box7 = ""
    price_pack_box8 = ""
    price_pack_box9 = ""
    price_pack_box10 = ""
    price_pack_box11 = ""
    price_pack_box12 = ""

    food = ""
    food_price = ""

#try and except is used here to avoid a null or empty value input by the user. A user can forget to input a price in pack value, which can break the code.
    if request.method == "POST":
        if request.POST["form"] == "form1":
            try:
                price_pack_box1 = int(request.POST.get("price1"))
                food = Food.objects.get(pk=1)
                food_price = food.food_price
                total_price1 = price_pack_box1*food_price
                print(total_price1)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form2":
            try:
                price_pack_box2 = int(request.POST.get("price2"))
                food = Food.objects.get(pk=2)
                food_price = food.food_price
                total_price2 = price_pack_box2*food_price
                print(total_price2)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form3":
            try:
                price_pack_box3 = int(request.POST.get("price3"))
                food = Food.objects.get(pk=3)
                food_price = food.food_price
                total_price3 = price_pack_box3*food_price
                print(total_price3)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form4":
            price_pack_box4 = int(request.POST.get("price4"))
            food = Food.objects.get(pk=4)
            food_price = food.food_price
            total_price4 = price_pack_box4*food_price
            print(total_price4)
        elif request.POST["form"] == "form5":
            try:
                price_pack_box5 = int(request.POST.get("price5"))
                food = Food.objects.get(pk=5)
                food_price = food.food_price
                total_price5 = price_pack_box5*food_price
                print(total_price5)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form6":
            try:
                price_pack_box6 = int(request.POST.get("price6"))
                food = Food.objects.get(pk=6)
                food_price = food.food_price
                total_price6 = price_pack_box6*food_price 
                print(total_price6)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form7":
            try:
                price_pack_box7 = int(request.POST.get("price7"))
                food = Food.objects.get(pk=7)
                food_price = food.food_price
                total_price7 = price_pack_box7*food_price
                print(total_price7)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form8":
            try:
                price_pack_box8 = int(request.POST.get("price8"))
                food = Food.objects.get(pk=8)
                food_price = food.food_price
                total_price8 = price_pack_box8*food_price
                print(total_price8)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form9":
            try:
                price_pack_box9 = int(request.POST.get("price9"))
                food = Food.objects.get(pk=9)
                food_price = food.food_price
                total_price9 = price_pack_box9*food_price
                print(total_price9)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form10":
            try:
                price_pack_box10 = int(request.POST.get("price10"))
                food = Food.objects.get(pk=10)
                food_price = food.food_price
                total_price10 = price_pack_box10*food_price
                print(total_price10)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form11":
            try:
                price_pack_box11 = int(request.POST.get("price11"))
                food = Food.objects.get(pk=11)
                food_price = food.food_price
                total_price11 = price_pack_box11*food_price
                print(total_price11)
            except ValueError:
                return render(request,'food_app/404.html',)
        elif request.POST["form"] == "form12":
            try:
                price_pack_box12 = int(request.POST.get("price12"))
                food = Food.objects.get(pk=12)
                food_price = food.food_price
                total_price12 = price_pack_box12*food_price
                print(total_price12)
            except ValueError:
                return render(request,'food_app/404.html',)

    my_dict = {'new_price1':[total_price1,price_pack_box1],'new_price2':[total_price2,price_pack_box2],
    'new_price3':[total_price3,price_pack_box3],'new_price4':[total_price4,price_pack_box4],
    'new_price5':[total_price5,price_pack_box5],'new_price6':[total_price6,price_pack_box6],
    'new_price7':[total_price7,price_pack_box7],'new_price8':[total_price8,price_pack_box8],
    'new_price9':[total_price9,price_pack_box9],'new_price10':[total_price10,price_pack_box10],
    'new_price11':[total_price11,price_pack_box11],'new_price12':[total_price12,price_pack_box12]}

    return render(request, 'food_app/price.html',context=my_dict)



def soup_box(request):

    my_soup_box = Soup.objects.all()

    egusi = my_soup_box.get(pk=1)
    egusi_item = egusi.soup_item
    egusi_mini = egusi.mini_box
    egusi_medium = egusi.medium_box
    egusi_mega = egusi.mega_box

    eforiro = my_soup_box.get(pk=2)
    eforiro_item = eforiro.soup_item
    eforiro_mini = eforiro.mini_box
    eforiro_medium = eforiro.medium_box
    eforiro_mega = eforiro.mega_box

    ogbona = my_soup_box.get(pk=3)
    ogbona_item = ogbona.soup_item
    ogbona_mini = ogbona.mini_box
    ogbona_medium = ogbona.medium_box
    ogbona_mega = ogbona.mega_box

    ila = my_soup_box.get(pk=4)
    ila_item = ila.soup_item
    ila_mini = ila.mini_box
    ila_medium = ila.medium_box
    ila_mega = ila.mega_box

    ewedu = my_soup_box.get(pk=5)
    ewedu_item = ewedu.soup_item
    ewedu_mini = ewedu.mini_box
    ewedu_medium = ewedu.medium_box
    ewedu_mega = ewedu.mega_box

    banga = my_soup_box.get(pk=6)
    banga_item = banga.soup_item
    banga_mini = banga.mini_box
    banga_medium = banga.medium_box
    banga_mega = banga.mega_box

    adi = my_soup_box.get(pk=7)
    adi_item = adi.soup_item
    adi_mini = adi.mini_box
    adi_medium = adi.medium_box
    adi_mega = adi.mega_box


    soup_box = {'soup_box1':[egusi_item,egusi_mini,egusi_medium,egusi_mega],
    'soup_box2':[eforiro_item,eforiro_mini,eforiro_medium,eforiro_mega],
    'soup_box3':[ogbona_item,ogbona_mini,ogbona_medium,ogbona_mega],
    'soup_box4':[ila_item,ila_mini,ila_medium,ila_mega],
    'soup_box5':[ewedu_item,ewedu_mini,ewedu_medium,ewedu_mega],
    'soup_box6':[banga_item,banga_mini,banga_medium,banga_mega],
    'soup_box7':[adi_item,adi_mini,adi_medium,adi_mega],}

    return render(request,'food_app/soup_box.html',context=soup_box)