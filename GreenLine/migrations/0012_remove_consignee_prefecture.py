# Generated by Django 4.1.7 on 2023-04-06 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GreenLine', '0011_consignee_prefecture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consignee',
            name='prefecture',
        ),
    ]