# Generated by Django 3.2.5 on 2024-06-04 05:53

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_status', models.CharField(choices=[('active', 'Aktif'), ('inactive', 'Pasif')], default='active', max_length=10, verbose_name='Durum')),
                ('firstname', models.CharField(max_length=200, verbose_name='Adı')),
                ('surname', models.CharField(max_length=200, verbose_name='Soyadı')),
                ('gender', models.CharField(choices=[('male', 'Erkek'), ('female', 'Kız')], default='male', max_length=10, verbose_name='Cinsiyeti')),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now, verbose_name='Doğum Tarihi')),
                ('date_of_interview', models.DateField(default=django.utils.timezone.now, verbose_name='Görüşme Taihi')),
                ('mobile_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message='Girilen cep telefonu numarası doğru formatta değil!', regex='^[0-9]{10,15}$')], verbose_name='Veli Cep Telefonu')),
                ('address', models.TextField(blank=True, verbose_name='Adres')),
                ('date_of_agreement', models.DateField(default=django.utils.timezone.now, verbose_name='Anlaşma Taihi')),
                ('other_name', models.CharField(blank=True, max_length=200, verbose_name='Verilen Ücret')),
                ('others', models.TextField(blank=True, verbose_name='Açıklama')),
            ],
        ),
    ]
