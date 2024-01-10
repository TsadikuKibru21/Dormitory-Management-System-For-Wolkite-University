import re
from dataclasses import field
from django import forms
from .models import *
from account.models import User,UserAccount
from django.contrib.auth.forms import PasswordChangeForm
class BlockTypeForm(forms.ModelForm):
    class Meta:
        model=BlockType
        fields='__all__'
class EmployeeForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['Id_no','FirstName','LastName','Gender','phone_no','is_Employee']
        widgets = {
        
            'Gender': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        phone_no = str(cleaned_data.get('phone_no'))

        if not phone_no.startswith('0') or len(phone_no) != 10 or not phone_no.isdigit():
            self.add_error('phone_no', 'Phone number must start with 0 and have 10 digits.All numbers must be numbers')
        return cleaned_data
class AddBlockForm(forms.ModelForm):
    class Meta:
        model=Block
        fields='__all__'
        widgets = {
            'Block_name': forms.TextInput(attrs={'class': 'form-control' ,'readonly':'True'}),
            'Block_type': forms.Select(attrs={'class': 'form-control'}),
            'Block_purpose': forms.Select(attrs={'class': 'form-control'}),
            
            'Block_Capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'Status': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_Block_Capacity(self):
        capacity = self.cleaned_data['Block_Capacity']
        if capacity < 1:
            raise forms.ValidationError("Block capacity must be greater than or equal to 1.")

        return capacity
class AddBlockForm1(forms.ModelForm):
    class Meta:
        model=Block
        fields='__all__'
        widgets = {
            'Block_name': forms.TextInput(attrs={'class': 'form-control' }),
            'Block_type': forms.Select(attrs={'class': 'form-control'}),
            'Block_purpose': forms.Select(attrs={'class': 'form-control'}),
            'Block_Capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'Status': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_Block_Capacity(self):
        capacity = self.cleaned_data['Block_Capacity']
        if capacity < 1:
            raise forms.ValidationError("Block capacity must be greater than or equal to 1.")

        return capacity
# class AddDorm(forms.ModelForm):
#     CHOICES = [('1','Active'),('0','Inactive')]
#     Status=forms.CharField(label='Status', widget=forms.RadioSelect(choices=CHOICES))
#     class Meta:
#         model=Dorm
#         fields='__all__'
class AddDorm(forms.ModelForm):
    class Meta:
        model = Dorm
        fields = '__all__'
        widgets = {
            'Block': forms.Select(attrs={'class': 'form-control'}),
            'Status': forms.Select(attrs={'class': 'form-control'}),
            'Floor': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_Capacity(self):
        capacity = self.cleaned_data['Capacity']

        if not capacity.isdigit():
            raise forms.ValidationError("Capacity must be a number.")

        capacity = int(capacity)

        if capacity < 1 or capacity > 100:
            raise forms.ValidationError("Capacity must be greater than 1 and less than 100.")

        return capacity
    
class AddPlacementForm(forms.ModelForm):
    class Meta:
        model=Placement
        fields=['Stud_id','Block']
        widgets = {
            'Stud_id': forms.Select(attrs={'class': 'form-control','disabled':'disabled'}),
            'Block': forms.Select(attrs={'class': 'form-control','disabled':'disabled'}),
           
        }
class PasswordChangingForm(PasswordChangeForm):
  
    class Meta:
        model= UserAccount
        fields=('old_password','new_password1','new_password2')
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control','type':'password'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control','type':'password'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control','type':'password'}),
           
        }

class AddAnnouncement(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['Title','Content','File','End_Date']
        widgets = {
            'Title': forms.TextInput(attrs={'class': 'form-control' }),
            'Content': forms.Textarea(attrs={'class': 'form-control'}),
            'File': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'Active_Date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'End_Date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }