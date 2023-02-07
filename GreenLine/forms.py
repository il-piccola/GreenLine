from django import forms
from django.forms import ModelForm
from .models import *

class LoginForm(forms.ModelForm) :
    mail = forms.CharField(label="メールアドレス", widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta :
        model = Member
        fields = ['mail', 'password', ]

