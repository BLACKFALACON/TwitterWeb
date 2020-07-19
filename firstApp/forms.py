from django import forms  
from firstApp.models import  Contact
  
class EmpForm(forms.ModelForm):  
    class Meta:  
        model = Contact  
        fields = [
            'konu',
            'mesaj',
        ] 
        
