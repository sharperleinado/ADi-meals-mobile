from django.shortcuts import render
from django.contrib.gis import gdal

# Create your views here.



def location(request):
    print(gdal.HAS_GDAL)

    return render(request,'geodjango/location.html',{})