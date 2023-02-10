from django import forms
from django.forms import ModelForm
from .models import *

class LoginForm(forms.ModelForm) :
    mail = forms.CharField(label="メールアドレス", widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta :
        model = Employee
        fields = ['mail', 'password', ]

class MainForm(forms.Form) :
    phone = forms.CharField(label="電話番号", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'01234567890', 'pattern':'^[0-9]+$'}))

