from django.urls import path
from . import views




app_name = 'geodjango'


urlpatterns = [
    path('location/',views.location, name="location")
]
