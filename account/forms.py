from django import forms

from account.models import Role,UserAccount,User,Settings
from django.contrib.auth.forms import PasswordChangeForm

class LoginForm(forms.Form):
    username=forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':"form-control border border-primary"
            }
        )
    )
    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':"form-control border border-primary"
            }
        )
    )
class RoleForm(forms.ModelForm):
     class Meta:
        model=Role
        fields='__all__'

class AddUserForm(forms.ModelForm):
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
# class DefaultUserForm(forms.Form):
#     class Meta:
#         model=UserAccount
#         fields='__all__'
class AddAccountForm(forms.ModelForm):
    class Meta:
        model=UserAccount
        fields=['username','Role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control' ,'readonly':'True'}),
            'Role': forms.Select(attrs={'class': 'form-control'}),
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

class UpdateSettingForm(forms.ModelForm):
    class Meta:
        model=Settings
        fields = '__all__'