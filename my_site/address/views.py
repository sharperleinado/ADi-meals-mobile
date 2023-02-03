from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import AddressForm,UpdateForm
from .models import UserAddress
from django.contrib import messages


# Create your views here.



def register_address(request):
    instance = ""
    try:
        form = AddressForm()
        if request.method == "POST":
            form = AddressForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user 
                instance.save()
                messages.success(request, "You have successfully added a shipping address!")
                return redirect('address:billing_address')
    except:
        pass
    
    return render(request,'address/register_address.html',{'form':form})



def billing_address(request):
    user = ""
    try:
        user = UserAddress.objects.get(user=request.user)
    except AttributeError:
        messages.error(request, "Please, create address before viewing address!")
        return redirect('address:register_address')
        #pass
    except:
        messages.error(request, "Please, create address before viewing address!")
        return redirect('address:register_address')
        #pass

    return render(request,'address/billing_address.html',{'form':user})




def update_address(request):
    form = UpdateForm()
    try:
        user = UserAddress.objects.get(user=request.user)
    except:
        messages.error(request, "Please, create an address before updating address!")
        return redirect('address:register_address') 
    try:
        if request.method == "POST":
            form = UpdateForm(request.POST)
            if form.is_valid():
                address = UserAddress.objects.get(user=request.user)
                address.user = request.user
                address.country = request.POST.get("country")
                address.state = request.POST.get("state")
                address.area = request.POST.get("area")
                address.city = request.POST.get("city")
                address.street_name = request.POST.get("street_name")
                address.save()
                messages.error(request, "You have successfully updated address.")
                return redirect('address:billing_address')
    except:
        pass
    
    return render(request,'address/update_address.html',{'form':form})

