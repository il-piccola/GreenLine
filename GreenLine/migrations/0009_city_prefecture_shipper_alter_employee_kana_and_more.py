# Generated by Django 4.1.7 on 2023-04-04 06:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GreenLine', '0008_alter_employee_kana'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=5)),
                ('name', models.CharField(default='', max_length=32)),
                ('kana', models.CharField(default='', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Prefecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=8)),
                ('kana', models.CharField(default='', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Shipper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=512)),
                ('kana', models.CharField(default='', max_length=1024)),
            ],
        ),
        migrations.AlterField(
            model_name='employee',
            name='kana',
            field=models.CharField(default='', max_length=64, validators=[django.core.validators.RegexValidator(message='カナはカタカナのみ入力できます', regex='^[ァ-ヴー]+$')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(default='', max_length=16, validators=[django.core.validators.RegexValidator(message='電話番号は半角数字のみ入力できます', regex='^[0-9]+$')]),
        ),
        migrations.AlterField(
            model_name='file',
            name='phone',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.CreateModel(
            name='Consignee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=512)),
                ('kana', models.CharField(default='', max_length=1024)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GreenLine.city')),
                ('shipper', models.ManyToManyField(to='GreenLine.shipper')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='prefecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GreenLine.prefecture'),
        ),
        migrations.AddField(
            model_name='file',
            name='consignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GreenLine.consignee'),
        ),
    ]