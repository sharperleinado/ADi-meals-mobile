from django import forms 


class PaymentForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    card_num = forms.CharField(max_length=20,required=True)
    expiry_month = forms.CharField(max_length=2,required=False)
    expiry_year = forms.CharField(max_length=4,required=False)
    cvv = forms.CharField(max_length=4, required=False)
