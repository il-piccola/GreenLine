# Generated by Django 4.1.7 on 2023-04-06 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GreenLine', '0010_organization_kana_alter_organization_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='consignee',
            name='prefecture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GreenLine.prefecture'),
        ),
    ]
