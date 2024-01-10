from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from account.models import UserAccount,User


class PasswordChangingForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
   
    class Meta:
        model= UserAccount
        fields=('old_password','new_password1','new_password2')