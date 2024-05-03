from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import AddressForm,UpdateForm
from django.contrib import messages
from cart.models import Cart
from .models import UserAddress,area,country_choice,city,state


# Create your views here.


def register_address(request):
    useraddress = ""
    
    try:
        useraddress = UserAddress.objects.get(user=request.user)
        if useraddress is not None:
            return redirect('authentication:account_info')
        else:
            pass
    except:
        pass
    
    if request.method == "POST":
        country_address = request.POST.get("country")
        state_address = request.POST.get("state")
        city_address = request.POST.get("city")
        area_address = request.POST.get("area")
        street_name_address = request.POST.get("street_name")
        useraddress = UserAddress.objects.create(user=request.user,country=country_address,state=state_address,city=city_address,area=area_address,street_name=street_name_address)
        messages.success(request, "You have successfully added a billing address!")
        messages.success(request, "You can proceed to order a meal now!")
        return redirect('authentication:mobile')
    
    return render(request,'address/register_address.html',{'country':country_choice,'state':state,'city':city,'area':area,})



def billing_address(request):
    user = ""
    try:
        user = UserAddress.objects.get(user=request.user)
    except AttributeError:
        messages.error(request, "Please, create address before viewing Home page!")
        return redirect('address:register_address')
    except:
        messages.error(request, "Please, create address before viewing Home page!")
        return redirect('address:register_address')

    return render(request,'address/billing_address.html',{'form':user})



def update_address(request):
    form = UpdateForm()
    try:
        user = UserAddress.objects.get(user=request.user)
    except:
        messages.error(request, "Please, create address before updating address!")
        return redirect('address:register_address') 
    try:
        if request.method == "POST":
            form = UpdateForm(request.POST)
            if form.is_valid():
                address = UserAddress.objects.get(user=request.user)
                address.user = request.user
                address.country = form.cleaned_data["country"]
                address.state = form.cleaned_data["state"]
                address.area = form.cleaned_data["area"]
                address.city = form.cleaned_data["city"]
                address.street_name = form.cleaned_data["street_name"]
                address.save()
                messages.error(request, "You have successfully updated address.")
                return redirect('address:billing_address')
    except:
        pass
    
    return render(request,'address/update_address.html',{'form':form})

