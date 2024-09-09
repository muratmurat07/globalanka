# Generated by Django 5.1 on 2024-09-08 14:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musteri',
            name='islem_yapan',
        ),
        migrations.RemoveField(
            model_name='musteri',
            name='musteri_no',
        ),
        migrations.AlterField(
            model_name='musteri',
            name='takip_eden',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='islem.takipedenkisi', verbose_name='Müşteri Temsilcisi'),
        ),
    ]
