from django.db import models
from django.db.models.signals import pre_save
from my_site.utils import unique_slug_generator
from django.contrib.contenttypes.fields import GenericRelation
from cart.models import CartItemsFood
from django.core.validators import FileExtensionValidator
from payments.models import Transactions




# Create your models here.
class Soup(models.Model):
    image = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    soup_item = models.CharField(max_length=30)
    mini_box_name = models.CharField(max_length=30,default="mini box")
    mini_box_price = models.DecimalField(max_digits=30,decimal_places=2,default=5000)
    medium_box_name = models.CharField(max_length=30,default="medium box")
    medium_box_price = models.DecimalField(max_digits=30,decimal_places=2,default=7000)
    mega_box_name = models.CharField(max_length=30,default="mega box")
    mega_box_price = models.DecimalField(max_digits=30,decimal_places=2,default=10000)
    slug = models.SlugField(max_length=250,null=True,blank=True)
    cart = GenericRelation(CartItemsFood)
    transactions = GenericRelation(Transactions)

    def __str__(self):
        my_soup = f"{self.soup_item}, {self.pk}"
        return my_soup
    


class Food(models.Model):
    image = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None)
    food_item = models.CharField(max_length=30)
    food_price = models.DecimalField(max_digits=30,decimal_places=2)
    slug = models.SlugField(max_length=250,null=True,blank=True)
    cart = GenericRelation(CartItemsFood)
    transactions = GenericRelation(Transactions)
    
    def __str__(self):
        my_food = f"{self.food_item}\n\n₦{self.food_price}\n{self.pk}"
        return my_food.capitalize()
    

def slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance)
        except:
            pass

pre_save.connect(slug_generator, sender=Food)
pre_save.connect(slug_generator, sender=Soup)  


'''
class Protein(models.Model):
    protein = models.CharField(max_length=50)
    
    def __str__(self):
        return self.protein
    
class SubProtein(models.Model):
    protein = models.ForeignKey(Protein,on_delete=models.CASCADE)
    subprotein = models.CharField(max_length=300)
    
    def __str__(self):
        return f"{self.subprotein} | {self.protein}"
    
class UserProtein(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    protein = models.ForeignKey(Protein,on_delete=models.CASCADE)
    subprotein = models.ForeignKey(SubProtein,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.protein.protein} | {self.subprotein.subprotein}"   
'''


