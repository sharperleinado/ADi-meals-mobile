from django.db import models

# Create your models here.
class Soup(models.Model):
    soup_item = models.CharField(max_length=30)
    mini_box = models.IntegerField()
    medium_box = models.IntegerField()
    mega_box = models.IntegerField()

    def __str__(self):
        my_soup = f"{self.soup_item}\n Mini price ₦{self.mini_box}\n Medium price ₦{self.medium_box}\n Mega price ₦{self.mega_box}"
        return my_soup


class Food(models.Model):
    food_item = models.CharField(max_length=30)
    food_price = models.IntegerField()

    def __str__(self):
        my_food = f"{self.food_item}\n\n₦{self.food_price}"
        return my_food