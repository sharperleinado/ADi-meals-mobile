'''
from django import forms
from food_app.models import UserProtein,SubProtein,Protein


class ProteinForm(forms.ModelForm):
    class Meta:
        model = UserProtein
        fields = ('protein','subprotein') 
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,kwargs)
        self.fields['subprotein'].queryset = SubProtein.objects.none()
    
        if 'protein' in self.data:
            try:
                protein_id = int(self.data.get('protein'))
                self.fields['subprotein'].queryset = NewSubProtein.objects.filter(protein=protein_id).order_by('name')
                
            except(ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['subprotein'].queryset = self.instance.protein.subprotein_set.order_by('name')'''



