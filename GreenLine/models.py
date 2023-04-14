import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
from .settings import *

# 部署マスタ
class Organization(models.Model) :
    name = models.CharField(max_length=512, default='')
    kana = models.CharField(max_length=1024, default='')
    def __str__(self) :
        return self.name

# ユーザマスタ
class Employee(models.Model) :
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, default='')
    kana_regex = RegexValidator(regex=r'^[ァ-ヴー]+$', message='カナはカタカナのみ入力できます')
    kana = models.CharField(validators=[kana_regex], max_length=64, default='')
    phone_regex = RegexValidator(regex=r'^[0-9]+$', message='電話番号は半角数字のみ入力できます')
    phone = models.CharField(validators=[phone_regex], max_length=16, default='')
    password = models.CharField(max_length=16, default='')
    auth = models.BooleanField(default=False)

# 都道府県マスタ
class Prefecture(models.Model) :
    name = models.CharField(max_length=8, default='')
    kana = models.CharField(max_length=16, default='')
    def __str__(self) :
        return self.name

# 市区町村マスタ
class City(models.Model) :
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, default='')
    name = models.CharField(max_length=32, default='')
    kana = models.CharField(max_length=64, default='')
    def __str__(self) :
        return self.name

# 荷主マスタ
class Shipper(models.Model) :
    name = models.CharField(max_length=512, default='')
    kana = models.CharField(max_length=1024, default='')
    def __str__(self) :
        return self.name

# 納品先マスタ
class Consignee(models.Model) :
    name = models.CharField(max_length=512, default='')
    kana = models.CharField(max_length=1024, default='')
    phone = models.CharField(max_length=16, default='')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    shipper = models.ManyToManyField(Shipper)
    def __str__(self) :
        return self.name

def upload_path(instance, filename) :
    base = os.path.splitext(os.path.basename(filename))[0]
    ext = os.path.splitext(os.path.basename(filename))[1]
    return instance.phone + '_' + base + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ext

# ファイルアップロードテーブル
class File(models.Model) :
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=16, default='')
    file = models.FileField(upload_to=upload_path, validators=[FileExtensionValidator(['pdf'])])
    def file_name(self) :
        return os.path.basename(self.file.name)
