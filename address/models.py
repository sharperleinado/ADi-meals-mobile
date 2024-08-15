from django.db import models
from authentication.models import User

# Create your models here.


country_choice = [("nigeria","Nigeria")]
state = [("ondo state","Ondo state")]
city = [("akure","Akure")]
area = [("alagbaka","Alagbaka"),("arakale","Arakale"),("araromi","Araromi"),
    ("futa north gate","Futa North Gate"),("futa south gate","Futa South Gate"),("igoba","Igoba"),
    ("ijapo","Ijapo"),("ijoka","Ijoka"),("irese","Irese"),
    ("isolo","Isolo"),("oba-ile","Oba-ile"),("oda","Oda"),
    ("oda road","Oda road"),("oke-aro","Oke-aro"),("oke-ijebu","Oke-Ijebu"),
    ("oke-ogba","Oke-Ogba"),("okuta-elerin_nla","Okuta-elerin_nla"),("onyarugbulem","Onyarugbulem"),
    ("orita","Orita-obele"),("owode","Owode"),("shagari","Shagari"),("others","Others")]




class UserAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    state = models.CharField(max_length=50)
    division = models.CharField(max_length=50, null=True)
    lga = models.CharField(max_length=50, null=True)
    lcda = models.CharField(max_length=50, null=True)
    street_name = models.CharField(max_length=300, null=True)

    def __str__(self):
        return f"{self.lga}, {self.lcda}, {self.street_name}."
    
    
