from django.shortcuts import render,redirect
from django.contrib import messages
from .models import UserAddress
import json
from django.http.response import JsonResponse


# Create your views here.



state_and_lga = {'lagos': {
            'badagry':{
                'ajeromi-Ifelodun': [['Ago Hausa', 800], ['Alaba Oro', 900], ['Awodi-Ora', 950], 
                                    ['Layeni', 1000], ['Mosafejo', 1050], ['Ojo Road', 1100],['Olodi', 1150], 
                                    ['Temidire I', 1200], ['Temidire II', 1250], ['Tolu', 1300], 
                                    ['Wilmer', 1350]],
                'amuwo-Odofin': [['Amuwo', 600], ['Amuwo-Odofin Housing Estate', 650], ['Mile 2', 700], 
                                    ['Festac 1', 750], ['Festac II', 800], ['Festac III', 850], 
                                    ['Ibeshe', 900], ['Igbologun', 950], ['Ijegun', 1000], ['Irede', 1050], 
                                    ['Kirikiri', 1100], ['Satellite', 1150]],
                 'badagry': [['Ajara', 600], ['Ajido', 650], ['Apa', 700], ['Awhanjigoh', 750], 
                                    ['Ibereko', 800], ['Ikoga', 850], ['Ilogbo-Araromi', 900], 
                                    ['Iworo Gbanko' ,950], ['Iya-Afin' ,1000], ['Keta-East', 1000], 
                                    ['Posukoh', 1050]],
                'ojo': [['Ajangbadi', 500], ['Etegbin', 550], ['Iba', 600], ['Idoluwo', 650], ['Ijanikin', 700], 
                                    ['Ilogbo', 750], ['Irewe', 800], ['Ojo Town', 800], ['Okokomaiko', 850], 
                                    ['Sabo', 900], ['Tafi', 950]],
                },
    

            'epe':{
                'ibeju-Lekki':  [['Orimedu II' ,500], ['Orimedu III', 550], ['Ibeju I', 600], 
                                ['Iwerekun II', 650], ['Lekki II', 700], ['Ibeju II', 750], ['Orimedu I', 800], 
                                ['Iwerekun I', 850], ['Siriwon I', 900], ['Igbekodo II', 950], 
                                ['Lekki I', 1000], ['Siriwon II', 1050], ['Igbekodo I', 1050]],
                'epe':  [['Abomiti', 500], ['Agbowa', 550], ['Agbowa Ikosi', 600], ['Ago Owu', 650], 
                        ['Ajaganabe', 700], ['Ejirin', 750], ['Etita/Ebode', 800], ['Ibonwon', 850], 
                        ['Ilara', 900], ['Ise', 950], ['Igbogun', 1000], ['Itoikin', 1050], ['Lagbade', 1100], 
                        ['Odomola', 1150], ['Odoragunsin', 1200], ['Oke-Balogun', 1250], ['Oriba', 1300], 
                        ['Ladaba', 1350], ['Orugbo', 1400], ['Poka', 1450], ['Popo-Oba', 1500]],
                'agege': [['Agbotikuyo', 500], ['Dopemu', 550], ['Darocha',600], ['Iloro', 650], ['Onipetesi', 700], 
                        ['Isale Odo', 750], ['Isale', 800], ['Idimangoro', 850], ['Keke', 900], ['Okekoto', 950], 
                        ['Oniwaya', 1000], ['Papa-Uku', 1050], ['Orile Agege', 1100], ['Oko Oba', 1200], 
                        ['Oyewole', 1250], ['Papa Ashafa', 1300], ['Tabon Tabon', 1350], ['Oko Oba', 1400]],
                'alimosho': [['Abule-Egba', 1000], ['Aboru', 1100], ['Meiran', 1200], ['Alagbado', 1300], 
                            ['Ayobo', 1400], ['Ijon Village (camp David)', 1500], ['Egbe', 1600], 
                            ['Agodo', 1700], ['Egbeda', 1800], ['Alimosho', 1900], ['Idimu', 2000], 
                            ['Isheri Olofin', 2100], ['Igando', 2200], ['Egan', 2300], 
                            ['Ikotun', 2400], ['Ijegun', 2500], ['Ipaja North', 2600], ['Ipaja South', 2700], 
                            ['Pleasure', 2800], ['Oke-Odo', 2900], ['Shasha', 3000], ['Akowonjo', 3100]],
                'ifako-Ijaiye': [['Ajegunle', 800], ['Akinde', 850], ['Animashaun', 900], ['Alakuko', 950], 
                                ['Kollington', 1000], ['Fagba', 1050], ['Akute Road', 1100], ['Ijaiye', 1200], 
                                ['Agbado', 1300], ['Kollington', 1400], ['Ijaiye', 1500], ['Ojokoro', 1600], 
                                ['Ijaye', 1700], ['Iju Isaga', 1800], ['Iju-Obawole', 1900], ['New Ifako', 2000], 
                                ['Oyemekun', 2100], ['Old Ifako', 2200], ['Karaole', 2300], 
                                ['Pamada', 2400], ['Aabule-Egba', 2500]],
                    },
            'ikeja': {
                'ikeja': [['Adekunle', 1000], ['Adeniyi Jones', 1200], ['Ogba', 1400], ['Airport', 1500], 
                        ['Onipetesi', 1600], ['Inilekere', 1700], ['Alausa', 1800], ['Oregun', 1900], 
                        ['Olusosun', 2000], ['Anifowoshe', 2100], ['Ikeja Gra', 2200], ['police Barracks', 2300], 
                        ['Ipodo', 2400], ['Seriki Aro', 2500], ['Ojodu', 2600], ['Agidingbi', 2700], ['Omole', 2800], 
                        ['Oke-Ira', 2800], ['Aguda', 2900], ['Onigbongbon', 3000], ['Wasimi', 3000], 
                        ['Opebi', 3000], ['Allen', 3000]],
                'kosofe': [['Agboyi I', 600], ['Agboyi II', 650], ['Anthony', 700], ['Ajao Estate', 700], 
                            ['Mende', 750], ['Maryland', 750], ['Ifako', 750], ['Soluyi', 800], 
                            ['Ikosi Ketu', 800], ['Mile 12', 800], ['Agiliti', 850], ['Maidan', 850], 
                            ['Isheri-Olowo-Ira', 900], ['Shangisha', 900], ['Magodo Phase II', 900], 
                            ['Ketu', 950], ['Alapere', 1000], ['Agidi', 1050], ['Orisigun', 1050], 
                            ['Kosofe', 1050], ['Aje', 1050], ['Logo', 1100], ['Akanimodo', 1100], ['Ojota', 1150], 
                            ['Ogudu', 1200], ['Owode Onirin', 1250], ['Ajegunle', 1300],['Odo-Ogun', 1350], 
                            ['Oworonshoki', 1400]],
                'mushin': [['Alakara', 800], ['Babalosa', 850], ['Babalosa', 850], ['Idi-araba', 850], 
                            ['Idi-Oro', 900], ['Odi-Olowu', 950], ['Ilasamaja', 950], ['Ilupeju', 950], 
                            ['Ilupeju Industrial Estate', 1000], ['Itire', 1050], ['Kayode', 1100], 
                            ['Fadeyi', 1150], ['Mushin', 1150], ['Atewolara', 1150], ['Ojuwoye', 1200], 
                            ['Olateju', 1250], ['Papa-Ajao', 1300]],
                'oshodi-Isolo': [['Ajao Estate', 800], ['Ilasamaja', 900], ['Ishagatedo', 950], ['Isolo', 1000], 
                                ['Mafoluku', 1050], ['Oke-Afa', 1100], ['Ejigbo', 1150], ['Okota', 1200], 
                                ['Orile-Oshodi', 1300], ['Oshodi', 1400], ['Bolade', 1400], ['Sogunle', 1500], 
                                ['Alasia', 1500]],
                'somolu': [['Abule-Okuta', 550], ['Ilaje', 600], ['Bariga', 650], ['Alade', 650],    
                            ['Bajulaiye', 700], ['Fola Agoro', 700], ['Bajulaiye', 750], 
                            ['Igbari-Akoka', 800], ['Gbagada Phase I Obanikoro', 850], ['Pedro', 900], 
                            ['Gbagada Phase II', 900], ['Apelehin', 950], ['Igbobi', 1000], ['Fadeyi', 1050], 
                            ['Ilaje', 1050], ['Akoka', 1100], ['Lad-Lak', 1150], ['Bariga', 1150], 
                            ['Mafowoku', 1200], ['Onipanu', 1250], ['Palmgrove', 1300], ['Ijebutedo', 1300]],
                },
            'ikorodu':{
                'ikorodu': [['Aga', 1000], ['Ijimu', 1100], ['Agbala', 1200], ['Agura', 1200], 
                            ['Iponmi', 1200], ['Baiyeku', 1250], ['Oreta', 1300], ['Erikorodu', 1300], ['Ibeshe', 1300], 
                            ['Igbogbo I', 1400], ['Igbogbo II', 1400], ['Ijede II', 1400], 
                            ['Ijede I', 1450], ['Imota 1', 1500], ['Imota II', 1500], ['Ipakodo', 1550], 
                            ['Isele I', 1550], ['Isele II', 1600], ['Isele III', 1650], ['Isiu', 1650], 
                            ['Odogunyan', 1600], ['Olorunda', 1600], ['Igbaga', 1650]],
                    },
            'lagos':{
                'apapa': [['Apapa I', 600], ['Apapa II', 650], ['Apapa III', 700], ['Apapa IV', 750], 
                        ['Gaskiya and Environs', 750], ['Ijora-Oloye', 800], ['Malu Road and Environs', 850], 
                        ['Olodan St. Olojowou', 850], 
                        ['Olatokunbo St. Iganmu', 900], ['Sari and Environs', 950]],
                'eti-Osa': [['Ado', 1000], ['Langbasa', 1100], ['Badore', 1200], ['Ajah', 1300], 
                            ['Sangotedo', 1400], ['Ikoyi I', 1450], ['Ikoyi II', 1450], 
                            ['Ilado', 1500], ['Ilasan Housing Estate', 1500], ['Lekki', 1550], 
                            ['Ikate and environs', 1600], ['Obalende', 1700], 
                            ['Victoria Island I', 1750], ['Victoria Island II', 1800]],
                'lagos Island': [['Agarawu', 800], ['Obadina', 800], ['Anikantamo', 850], ['Eiyekole', 850], 
                                ['Epetedo', 900], ['Idumota', 900], ['Oke', 950],[ 'Iduntafa', 950], 
                                ['Ilupesi', 1000], ['Isale-agbede', 1100], ['Lafiaji', 1150], ['Ebute', 1150], 
                                ['Oju-oto', 1200], ['Oko-awo', 1200], ['Oko-faji', 1250], ['Olosun', 1200], 
                                ['Olowogbowo', 1250], ['Elegbata', 1300], ['Olushi', 1300], ['Kakawa', 1300], 
                                ['Oluwole', 1300], ['Onikan', 1350], ['Popo-Aguda', 1400], ['Sandgrouse', 1500]],
                'lagos Mainland': [['Alagomeji', 1200], ['Epetedo', 1300], ['Glover', 1300], 
                                ['Ebute Metta', 1350], ['Iwaya', 1350], ['Maroko', 1350], ['Metta', 1350], 
                                ['Oko-Baba', 1400], ['Olaleye Village', 1400], ['Otto', 1400], ['Iddo', 1400], 
                                ['Oyadiran Estate', 1450], ['Abule-Oja', 1500], ['Oyingbo Market', 1500], 
                                ['Metta', 1550], ['Yaba', 1600], ['Igbobi', 1650]],
                    'surulere': [['Adeniran', 900], ['Ogunsanya', 900], ['Aguda', 950], ['Akinhanmi', 950], 
                                ['Cole', 1000], ['Coker', 1050], ['Igbaja', 1100], 
                                ['Stadium', 1100], ['Ijeshatedo', 1100], ['Ikate', 1150], 
                                ['Iponri Housing Estate', 1200], ['Eric Moore', 1200], ['Itire', 1250], 
                                ['Orile', 1250], ['Shitta', 1300], ['Ogunlana Drive', 1300], ['Yaba', 1400], 
                                ['Ojuelegba', 1450]]
                                },       
                }
                }



'''
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
                }'''



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
        return redirect('food_app:soupbox')
    
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

