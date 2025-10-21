from django.contrib import admin 
#from .models import User 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserCreationForm,UserAdminChangeForm
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()


admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserCreationForm


    list_display = ["email","mobile","admin"]
    list_filter = ["email","admin"]
    fieldsets = (
        (None, {
            "fields": ("first_name",
                       "last_name",
                       "email",
                       "mobile",
            ),
        }),
        ("Personal info", {
            "fields": (),
        }),
        ("Permission", {
            "fields": ("is_active","staff","admin",),
        }),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("first_name","last_name","email","mobile","password","password_2"),
        }),
    )
    
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = ()

admin.site.register(User,UserAdmin)

