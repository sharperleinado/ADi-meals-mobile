from django.contrib import admin
from .models import Food,Soup,Protein,SubProtein,UserProtein

# Register your models here.


admin.site.register(Food)
admin.site.register(Soup)
admin.site.register(Protein)
admin.site.register(SubProtein)
admin.site.register(UserProtein)



