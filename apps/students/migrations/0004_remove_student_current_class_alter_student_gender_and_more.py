# Generated by Django 5.1 on 2024-08-25 15:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20240603_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='current_class',
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('İlkokul', 'İlkokul'), ('Ortaokul', 'Ortaokul'), ('Lise', 'Lise'), ('Üniversite', 'Üniversite'), ('Yüksek Lisans', 'Yüksek Lisans'), ('Doktora', 'Doktora')], default='male', max_length=100, verbose_name='Öğrenim Durumu'),
        ),
        migrations.AlterField(
            model_name='student',
            name='other_name',
            field=models.IntegerField(default=0, verbose_name='Taksit Sayısı'),
        ),
        migrations.AlterField(
            model_name='student',
            name='parent_mobile_number',
            field=models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message='Girilen cep telefonu numarası doğru formatta değil!', regex='^[0-9]{10,15}$')], verbose_name='Telefon Numarası'),
        ),
    ]