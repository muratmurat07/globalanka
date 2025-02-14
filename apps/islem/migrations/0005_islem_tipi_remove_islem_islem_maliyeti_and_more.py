# Generated by Django 5.1 on 2024-09-08 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0004_remove_musteri_musteri_no_alter_islem_islem_yapan_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Islem_Tipi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('islem_adi', models.CharField(max_length=200, verbose_name='Adı')),
                ('islem_maliyeti', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='İşlem Maliyeti')),
            ],
        ),
        migrations.RemoveField(
            model_name='islem',
            name='islem_maliyeti',
        ),
        migrations.AlterField(
            model_name='islem',
            name='toplam_borc',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ücreti'),
        ),
        migrations.AlterField(
            model_name='musteri',
            name='adres',
            field=models.CharField(max_length=200, verbose_name='Adres'),
        ),
        migrations.AlterField(
            model_name='islem',
            name='islem_tipi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='islem.islem_tipi', verbose_name='Yapılan İşlem'),
        ),
    ]
