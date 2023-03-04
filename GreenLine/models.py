import os
import random
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
from .settings import *

class Organization(models.Model) :
    name = models.CharField(max_length=200, default='')
    def __str__(self) :
        return self.name

class Employee(models.Model) :
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    kana_regex = RegexValidator(regex=r'^[ァ-ヴ]+$', message='カナはカタカナのみ入力できます')
    kana = models.CharField(validators=[kana_regex], max_length=200, default='')
    phone_regex = RegexValidator(regex=r'^[0-9]+$', message='電話番号は半角数字のみ入力できます')
    phone = models.CharField(validators=[phone_regex], max_length=200, default='')
    password = models.CharField(max_length=16, default='')
    auth = models.BooleanField(default=False)

def upload_path(instance, filename) :
    filename = instance.phone + os.path.splitext(filename)[1]
    return filename

class File(models.Model) :
    phone = models.CharField(max_length=200, default='')
    file = models.FileField(upload_to=upload_path, validators=[FileExtensionValidator(['pdf'])])
