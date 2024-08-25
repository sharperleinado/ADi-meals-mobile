from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from cart.models import Cart
from .models import UserAddress,area,country_choice,city,state
import json
from django.http.response import JsonResponse


# Create your views here.

state_and_lga = {'lagos': {
            'badagry':{
                'ajeromi-Ifelodun': ['Ago Hausa', 'Alaba Oro', 'Awodi-Ora', 'Layeni', 'Mosafejo', 'Ojo Road',
                                    'Olodi', 'Temidire I', 'Temidire II', 'Tolu', 'Wilmer'],
                'amuwo-Odofin': ['Amuwo', 'Amuwo-Odofin Housing Estate', 'Mile 2', 'Festac 1', 'Festac II',
                                'Festac III', 'Ibeshe', 'Igbologun', 'Ijegun', 'Irede', 'Kirikiri', 'Satellite'],
                 'badagry': ['Ajara', 'Ajido', 'Apa', 'Awhanjigoh', 'Ibereko', 'Ikoga', 'Ilogbo-Araromi', 
                             'Iworo Gbanko', 'Iya-Afin', 'Keta-East', 'Posukoh'],
                'ojo': ['Ajangbadi', 'Etegbin', 'Iba', 'Idoluwo', 'Ijanikin', 'Ilogbo', 'Irewe', 'Ojo Town', 
                        'Okokomaiko', 'Sabo', 'Tafi'],
                },
    

            'epe':{
                'ibeju-Lekki':  ['Orimedu II', 'Orimedu III', 'Ibeju I', 'Iwerekun II', 'Lekki II', 
                                'Ibeju II', 'Orimedu I', 'Iwerekun I', 'Siriwon I', 'Igbekodo II', 
                                'Lekki I', 'Siriwon II', 'Igbekodo I'],
                'epe':  ['Abomiti', 'Agbowa', 'Agbowa Ikosi', 'Ago Owu', 'Ajaganabe', 'Ejirin', 'Etita/Ebode', 
                        'Ibonwon', 'Ilara', 'Ise', 'Igbogun', 'Itoikin', 'Lagbade', 'Odomola', 'Odoragunsin', 
                        'Oke-Balogun', 'Oriba', 'Ladaba', 'Orugbo', 'Poka', 'Popo-Oba'],
                'agege': ['Agbotikuyo', 'Dopemu', 'Darocha', 'Iloro', 'Onipetesi', 'Isale Odo', 
                        'Isale', 'Idimangoro', 'Keke', 'Okekoto', 'Oniwaya', 'Papa-Uku', 'Orile Agege', 
                        'Oko Oba', 'Oyewole', 'Papa Ashafa', 'Tabon Tabon', 'Oko Oba'],
                'alimosho': ['Abule-Egba', 'Aboru', 'Meiran', 'Alagbado', 'Ayobo', 'Ijon Village (camp David)', 
                            'Egbe', 'Agodo', 'Egbeda', 'Alimosho', 'Idimu', 'Isheri Olofin', 'Igando', 'Egan', 
                            'Ikotun', 'Ijegun', 'Ipaja North', 'Ipaja South', 'Pleasure', 'Oke-Odo', 'Shasha', 
                            'Akowonjo'],
                'ifako-Ijaiye': ['Ajegunle', 'Akinde', 'Animashaun', 'Alakuko', 'Kollington', 'Fagba', 
                                'Akute Road', 'Ijaiye', 'Agbado', 'Kollington', 'Ijaiye', 'Ojokoro', 'Ijaye', 
                                'Iju Isaga', 'Iju-Obawole', 'New Ifako', 'Oyemekun', 'Old Ifako', 'Karaole', 
                                'Pamada', 'Aabule-Egba'],
                    },
            'ikeja': {
                'ikeja': ['Adekunle', 'Adeniyi Jones', 'Ogba', 'Airport', 'Onipetesi', 'Inilekere', 
                        'Alausa', 'Oregun', 'Olusosun', 'Anifowoshe', 'Ikeja Gra', 'police Barracks', 
                        'Ipodo', 'Seriki Aro', 'Ojodu', 'Agidingbi', 'Omole', 'Oke-Ira', 'Aguda', 
                        'Onigbongbon', 'Wasimi', 'Opebi', 'Allen'],
                'kosofe': ['Agboyi I', 'Agboyi II', 'Anthony', 'Ajao Estate', 'Mende', 'Maryland', 
                            'Ifako', 'Soluyi', 'Ikosi Ketu', 'Mile 12', 'Agiliti', 'Maidan', 
                            'Isheri-Olowo-Ira', 'Shangisha', 'Magodo Phase II', 'Ketu', 'Alapere', 
                            'Agidi', 'Orisigun', 'Kosofe', 'Aje', 'Logo', 'Akanimodo', 'Ojota', 'Ogudu', 
                            'Owode Onirin', 'Ajegunle','Odo-Ogun', 'Oworonshoki'],
                'mushin': ['Alakara', 'Babalosa', 'Babalosa', 'Idi-araba', 'Idi-Oro', 'Odi-Olowu', 
                            'Ilasamaja', 'Ilupeju', 'Ilupeju Industrial Estate', 'Itire', 'Kayode', 
                            'Fadeyi', 'Mushin', 'Atewolara', 'Ojuwoye', 'Olateju', 'Papa-Ajao'],
                'oshodi-Isolo': ['Ajao Estate', 'Ilasamaja', 'Ishagatedo', 'Isolo', 'Mafoluku', 'Oke-Afa', 
                                    'Ejigbo', 'Okota', 'Orile-Oshodi', 'Oshodi', 'Bolade', 'Sogunle', 'Alasia'],
                'somolu': ['Abule-Okuta', 'Ilaje', 'Bariga', 'Alade', 'Bajulaiye', 'Fola Agoro', 
                            'Bajulaiye', 'Igbari-Akoka', 'Gbagada Phase I Obanikoro', 'Pedro', 
                            'Gbagada Phase II', 'Apelehin', 'Igbobi', 'Fadeyi', 'Ilaje', 'Akoka', 'Lad-Lak', 
                            'Bariga', 'Mafowoku', 'Onipanu', 'Palmgrove', 'Ijebutedo'],
                },
            'ikorodu':{
                'ikorodu': ['Aga', 'Ijimu', 'Agbala', 'Agura', 'Iponmi', 'Baiyeku', 'Oreta', 'Erikorodu', 
                            'Ibeshe', 'Igbogbo I', 'Igbogbo II', 'Ijede II', 'Ijede I', 'Imota 1', 'Imota II', 
                            'Ipakodo', 'Isele I', 'Isele II', 'Isele III', 'Isiu', 'Odogunyan', 'Olorunda', 
                            'Igbaga'],
                    },
            'lagos':{
                'apapa': ['Apapa I', 'Apapa II', 'Apapa III', 'Apapa IV', 'Gaskiya and Environs', 
                        'Ijora-Oloye', 'Malu Road and Environs', 'Olodan St. Olojowou', 
                        'Olatokunbo St. Iganmu', 'Sari and Environs'],
                'eti-Osa': ['Ado', 'Langbasa', 'Badore', 'Ajah', 'Sangotedo', 'Ikoyi I', 'Ikoyi II', 
                            'Ilado', 'Ilasan Housing Estate', 'Lekki', 'Ikate and environs', 'Obalende', 
                            'Victoria Island I', 'Victoria Island II'],
                'lagos Island': ['Agarawu', 'Obadina', 'Anikantamo', 'Eiyekole', 'Epetedo', 'Idumota', 
                                'Oke', 'Iduntafa', 'Ilupesi', 'Isale-agbede', 'Lafiaji', 'Ebute', 
                                'Oju-oto', 'Oko-awo', 'Oko-faji', 'Olosun', 'Olowogbowo', 'Elegbata', 
                                'Olushi', 'Kakawa', 'Oluwole', 'Onikan', 'Popo-Aguda', 'Sandgrouse'],
                'lagos Mainland': ['Alagomeji', 'Epetedo', 'Glover', 'Ebute Metta', 'Iwaya', 'Maroko', 
                                'Metta', 'Oko-Baba', 'Olaleye Village', 'Otto', 'Iddo', 'Oyadiran Estate', 
                                'Abule-Oja', 'Oyingbo Market', 'Metta', 'Yaba', 'Igbobi'],
                    'surulere': ['Adeniran', 'Ogunsanya', 'Aguda', 'Akinhanmi', 'Cole', 'Coker', 'Igbaja', 
                                'Stadium', 'Ijeshatedo', 'Ikate', 'Iponri Housing Estate Moore', 'Itire', 
                                'Orile', 'Shitta', 'Ogunlana Drive', 'Yaba', 'Ojuelegba']
                                },       
                }
                }



def register_address(request):
    useraddress = ""
    
    try:
        useraddress = UserAddress.objects.get(user=request.user)
        if useraddress is not None:
            messages.info(request, "You already have an address registered!")
            return redirect('authentication:account_info')
        else:
            pass
    except:
        pass
        
    if request.method == "POST":
        state = request.POST.get("state")
        division = request.POST.get("division")
        lga = request.POST.get("lga")
        lcda = request.POST.get("lcda")
        street_name = request.POST.get("street_name")
        useraddress = UserAddress.objects.get_or_create(user=request.user,state=state,division=division,lga=lga,lcda=lcda,street_name=street_name)
        messages.success(request, "You have successfully created address!")
        return redirect('authentication:mobile')
    
    return render(request,'address/register_address.html',{'state_lga':state_and_lga.items()})



def billing_address(request):
    user = ""
    try:
        user = UserAddress.objects.get(user=request.user)
    except AttributeError:
        messages.error(request, "Please, create address before viewing address page!")
        return redirect('address:register_address')
    except:
        messages.error(request, "Please, create address before viewing address page!")
        return redirect('address:register_address')

    return render(request,'address/billing_address.html',{'form':user})


def change_address(request):#division
    if request.method == "POST":
        data = json.loads(request.body)
        address_value = data.get('division_id')
        divisions = state_and_lga.get(address_value, {})
        response_data = list(divisions.keys())
        return JsonResponse(response_data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def change_address_division(request):#lga
    if request.method == "POST":
        data = json.loads(request.body)
        division_value = data.get('lga_id')
        selected_state = data.get('state')
        divisions_selsect = state_and_lga.get(selected_state, {})
        lga = divisions_selsect.get(division_value).keys()
        return JsonResponse(list(lga), safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def change_address_lga(request):#lcda
    if request.method == "POST":
        data = json.loads(request.body)
        lcda = data.get('lcda_id')
        selected_state = data.get('state')
        selected_division = data.get('division')
        lga = data.get('lga')
        state = state_and_lga.get(selected_state, {})
        lcda_list = state.get(selected_division).get(lga)

        return JsonResponse(lcda_list, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


'''
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
    
    return render(request,'address/update_address.html',{'form':form})'''

