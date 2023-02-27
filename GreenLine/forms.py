from django import forms
from django.forms import ModelForm
from .models import *

class LoginForm(forms.ModelForm) :
    phone = forms.CharField(label="電話番号", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}))
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta :
        model = Employee
        fields = ['phone', 'password', ]

class MainForm(forms.Form) :
    phone = forms.CharField(label="電話番号", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'01234567890', 'pattern':'^[0-9]+$'}))

class PasswordForm(forms.Form) :
    old = forms.CharField(label="旧パスワード", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new = forms.CharField(label="新パスワード", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm = forms.CharField(label="新パスワード(確認)", widget=forms.PasswordInput(attrs={'class':'form-control'}))
