from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,mobile,password=None):
        if not email:
            raise ValueError("User must have an email address!")
        user = self.model(first_name=first_name,last_name=last_name,email=self.normalize_email(email),mobile=mobile)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self,first_name,last_name,email,mobile,password):
        user = self.create_user(first_name,last_name,email,mobile,password)
        user.staff = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,email,mobile,password):
        user = self.create_user(first_name,last_name,email,mobile,password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = PhoneNumberField(unique=True)

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','mobile']


    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
