from django import forms
from .models import Properties

class Property_Register_Form(forms.ModelForm):
    class Meta:
        model=Properties
        fields='__all__'

        widgets = {
            'property_category': forms.Select(attrs={'class': 'form-control'}),
            'block': forms.TextInput(attrs={'class': 'form-control','disable':'True' ,'readonly':'True'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
        }
