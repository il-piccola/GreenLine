from django import forms
from django.forms import ModelForm
from .models import *

class LoginForm(forms.ModelForm) :
    phone = forms.CharField(label="従業員電話番号", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}))
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta :
        model = Employee
        fields = ['phone', 'password', ]

class MainForm(forms.Form) :
    phone = forms.CharField(label="納品先電話番号", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'01234567890', 'pattern':'^[0-9]+$'}))

class PasswordForm(forms.Form) :
    new = forms.CharField(label="新パスワード", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm = forms.CharField(label="新パスワード(確認)", widget=forms.PasswordInput(attrs={'class':'form-control'}))

class EmployeeForm(forms.ModelForm) :
    organization = forms.ModelChoiceField(label="所属", queryset=Organization.objects, widget=forms.Select(attrs={'class':'form-select'}))
    name = forms.CharField(label="氏名", widget=forms.TextInput(attrs={'class':'form-control'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[ァ-ヴー]+$'}))
    phone = forms.CharField(label="従業員電話番号", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}))
    password = forms.CharField(label="パスワード", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}))
    auth = forms.BooleanField(label="管理者権限", required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    class Meta :
        model = Employee
        fields = ['organization', 'name', 'kana', 'phone', 'password', 'auth', ]
    def get_organization(self) :
        return self.instance.organization.name

class AddEmployeeForm(forms.ModelForm) :
    organization = forms.ModelChoiceField(label="所属", queryset=Organization.objects, widget=forms.Select(attrs={'class':'form-select'}))
    name = forms.CharField(label="氏名", widget=forms.TextInput(attrs={'class':'form-control'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[ァ-ヴー]+$'}))
    phone = forms.CharField(label="従業員電話番号", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}))
    dummy = forms.CharField(label="パスワード", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'disabled':'disabled'}))
    auth = forms.BooleanField(label="管理者権限", required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    class Meta :
        model = Employee
        fields = ['organization', 'name', 'kana', 'phone', 'auth', ]
    def get_organization(self) :
        return self.instance.organization.name

class UploadForm(forms.ModelForm) :
    phone = forms.CharField(label="納品先電話番号", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}))
    file = forms.FileField(label="PDFファイル", widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta :
        model = File
        fields = ['phone', 'file', ]

class OrganizationForm(forms.ModelForm) :
    name = forms.CharField(label="名称", widget=forms.TextInput(attrs={'class':'form-control'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[ァ-ヴー]+$'}))
    class Meta :
        model = Organization
        fields = ['name', 'kana', ]

class ShipperForm(forms.ModelForm) :
    name = forms.CharField(label="名称", widget=forms.TextInput(attrs={'class':'form-control'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[ァ-ヴー]+$'}))
    class Meta :
        model = Shipper
        fields = ['name', 'kana', ]

class ConsigneeForm(forms.ModelForm) :
    name = forms.CharField(label="名称", widget=forms.TextInput(attrs={'class':'form-control'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[ァ-ヴー]+$'}))
    phone = forms.CharField(label="電話番号", widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}))
    prefecture = forms.ModelChoiceField(label="都道府県", queryset=Prefecture.objects.all(), widget=forms.Select(attrs={'class':'form-control prefecture'}))
    city = forms.IntegerField(label="市区町村", widget=forms.HiddenInput(attrs={'class':'city'}))
    shipper = forms.ModelMultipleChoiceField(label="メーカー(荷主)", queryset=Shipper.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    class Meta :
        model = Consignee
        fields = ['name', 'kana', 'phone', 'city', 'shipper', ]
