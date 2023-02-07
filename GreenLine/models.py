from django.db import models

class Organization(models.Model) :
    name = models.CharField(max_length=200, default='')

class Member(models.Model) :
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    kana = models.CharField(max_length=200, default='')
    mail = models.EmailField(max_length=200, default='')
    password = models.CharField(max_length=200, default='')
