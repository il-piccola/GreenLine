import os
from django.db import models
from django.core.validators import RegexValidator
from .settings import *

class Organization(models.Model) :
    name = models.CharField(max_length=200, default='')

class Employee(models.Model) :
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    kana = models.CharField(max_length=200, default='')
    phone_regex = RegexValidator(regex=r'^[0-9]+$', message='電話番号は半角数字のみ入力できます')
    phone = models.CharField(validators=[phone_regex], max_length=200, default='')
    password = models.CharField(max_length=200, default='')
    auth = models.BooleanField(default=False)

def upload_path(instance, filename) :
    newname = instance.phone
    return os.path.join('pdf', newname)

class File(models.Model) :
    phone = models.CharField(max_length=200, default='')
    file = models.FileField(upload_to=upload_path)
    def get_ext(self) :
        return os.path.splitext(self.file)[1][:1]
    def get_path(self) :
        return os.path.join(MEDIA_ROOT, self.file.path)
