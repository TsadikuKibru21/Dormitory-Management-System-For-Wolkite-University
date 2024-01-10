from django import forms
from .models import *
from account.models import User,UserAccount


class StudentForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['Id_no','FirstName','LastName','Gender','phone_no','stream','collage','Department','Year_of_Student','Campus','Emergency_responder_name','Emergency_responder_address','Emergency_responder_phone_no','Disability']
        widgets = {
        
            'Gender': forms.Select(attrs={'class': 'form-control' }),
            'stream': forms.Select(attrs={'class': 'form-control'}),
            'Campus': forms.Select(attrs={'class': 'form-control'}),
            'Disability': forms.Select(attrs={'class': 'form-control'}),
        }