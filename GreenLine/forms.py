from django import forms
from django.forms import ModelForm
from .models import *

class LoginForm(forms.ModelForm) :
    phone = forms.CharField(label="従業員電話番号", widget=forms.TextInput(attrs={'class':'form-control phone', 'pattern':'^[0-9]+$'}))
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(attrs={'class':'form-control password'}))
    class Meta :
        model = Employee
        fields = ['phone', 'password', ]

class MainForm(forms.Form) :
    class SearchChoices(models.TextChoices) :
        name = 'name', '納品先名'
        phone = 'phone', '電話番号'
        city = 'city', '市区町村'
    shipper = forms.ModelChoiceField(label="メーカー(荷主)", queryset=Shipper.objects.all(), widget=forms.Select(attrs={'class':'form-select shipper'}))
    radio = forms.ChoiceField(label='', choices=SearchChoices.choices, required=True, widget=forms.widgets.RadioSelect(attrs={'class':'form-check-input radio'}))
    name = forms.CharField(label='納品先名', required=False, widget=forms.TextInput(attrs={'class':'form-control name'}))
    phone = forms.CharField(label='電話番号', required=False, widget=forms.TextInput(attrs={'class':'form-control phone'}))
    prefecture = forms.IntegerField(label="都道府県", widget=forms.HiddenInput(attrs={'class':'prefecture'}))
    city = forms.CharField(label="市区町村", widget=forms.HiddenInput(attrs={'class':'city'}))
    town = forms.CharField(label="町域", widget=forms.HiddenInput(attrs={'class':'town'}))
    consignee = forms.IntegerField(label="納品先", widget=forms.HiddenInput(attrs={'class':'consignee'}))

class PasswordForm(forms.Form) :
    new = forms.CharField(label="新パスワード", widget=forms.PasswordInput(attrs={'class':'form-control new'}))
    confirm = forms.CharField(label="新パスワード(確認)", widget=forms.PasswordInput(attrs={'class':'form-control confirm'}))

class EmployeeForm(forms.ModelForm) :
    organization = forms.ModelChoiceField(label="所属", queryset=Organization.objects, widget=forms.Select(attrs={'class':'form-select organization'}))
    name = forms.CharField(label="氏名", widget=forms.TextInput(attrs={'class':'form-control name'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control kana', 'pattern':'^[ァ-ヴー]+$'}))
    phone = forms.CharField(label="従業員電話番号", widget=forms.TextInput(attrs={'class':'form-control phone', 'pattern':'^[0-9]+$'}))
    password = forms.CharField(label="パスワード", widget=forms.TextInput(attrs={'class':'form-control password', 'pattern':'^[0-9]+$'}))
    auth = forms.BooleanField(label="管理者権限", required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input auth'}))
    class Meta :
        model = Employee
        fields = ['organization', 'name', 'kana', 'phone', 'password', 'auth', ]
    def get_organization(self) :
        return self.instance.organization.name

class AddEmployeeForm(forms.ModelForm) :
    organization = forms.ModelChoiceField(label="所属", queryset=Organization.objects, widget=forms.Select(attrs={'class':'form-select organization'}))
    name = forms.CharField(label="氏名", widget=forms.TextInput(attrs={'class':'form-control name'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control kana', 'pattern':'^[ァ-ヴー]+$'}))
    phone = forms.CharField(label="従業員電話番号", widget=forms.TextInput(attrs={'class':'form-control phone', 'pattern':'^[0-9]+$'}))
    dummy = forms.CharField(label="パスワード", required=False, widget=forms.TextInput(attrs={'class':'form-control dummy', 'disabled':'disabled'}))
    auth = forms.BooleanField(label="管理者権限", required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input auth'}))
    class Meta :
        model = Employee
        fields = ['organization', 'name', 'kana', 'phone', 'auth', ]
    def get_organization(self) :
        return self.instance.organization.name

class UploadForm(forms.ModelForm) :
    zip = forms.CharField(label="郵便番号", widget=forms.TextInput(attrs={'class':'form-control zip', 'pattern':'^[0-9]+$'}))
    prefecture = forms.ModelChoiceField(label="都道府県", queryset=Prefecture.objects.all(), widget=forms.Select(attrs={'class':'form-control prefecture'}))
    city = forms.CharField(label="市区町村", widget=forms.HiddenInput(attrs={'class':'city'}))
    town = forms.CharField(label="町域", widget=forms.HiddenInput(attrs={'class':'town'}))
    consignee = forms.IntegerField(label="納品先", widget=forms.HiddenInput(attrs={'class':'consignee'}))
    file = forms.FileField(label="PDFファイル", widget=forms.FileInput(attrs={'class':'form-control file'}))
    class Meta :
        model = File
        fields = ['file', ]

class OrganizationForm(forms.ModelForm) :
    name = forms.CharField(label="名称", widget=forms.TextInput(attrs={'class':'form-control name'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control kana', 'pattern':'^[ァ-ヴー]+$'}))
    class Meta :
        model = Organization
        fields = ['name', 'kana', ]

class ShipperForm(forms.ModelForm) :
    name = forms.CharField(label="名称", widget=forms.TextInput(attrs={'class':'form-control name'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control kana', 'pattern':'^[ァ-ヴー]+$'}))
    class Meta :
        model = Shipper
        fields = ['name', 'kana', ]

class ConsigneeForm(forms.ModelForm) :
    name = forms.CharField(label="名称", widget=forms.TextInput(attrs={'class':'form-control name'}))
    kana = forms.CharField(label="カナ", widget=forms.TextInput(attrs={'class':'form-control kana', 'pattern':'^[ァ-ヴー]+$'}))
    phone = forms.CharField(label="電話番号", widget=forms.TextInput(attrs={'class':'form-control phone', 'pattern':'^[0-9]+$'}))
    zip = forms.CharField(label="郵便番号", widget=forms.TextInput(attrs={'class':'form-control zip', 'pattern':'^[0-9]+$'}))
    prefecture = forms.ModelChoiceField(label="都道府県", queryset=Prefecture.objects.all(), widget=forms.Select(attrs={'class':'form-control prefecture'}))
    city = forms.CharField(label="市区町村", widget=forms.HiddenInput(attrs={'class':'city'}))
    town = forms.CharField(label="町域", widget=forms.HiddenInput(attrs={'class':'town'}))
    address = forms.CharField(label="以降の住所", widget=forms.TextInput(attrs={'class':'form-control address'}))
    shipper = forms.ModelMultipleChoiceField(label="メーカー(荷主)", queryset=Shipper.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control shipper'}))
    class Meta :
        model = Consignee
        fields = ['name', 'kana', 'phone', 'address', 'shipper', ]
