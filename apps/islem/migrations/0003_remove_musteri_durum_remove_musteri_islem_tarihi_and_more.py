# Generated by Django 5.1 on 2024-09-08 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0002_remove_musteri_islem_yapan_remove_musteri_musteri_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musteri',
            name='durum',
        ),
        migrations.RemoveField(
            model_name='musteri',
            name='islem_tarihi',
        ),
        migrations.AddField(
            model_name='musteri',
            name='musteri_no',
            field=models.CharField(default=1, max_length=100, unique=True, verbose_name='Müşteri Numarası'),
            preserve_default=False,
        ),
    ]
