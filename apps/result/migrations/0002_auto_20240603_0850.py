# Generated by Django 3.2.5 on 2024-06-03 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corecode', '0005_auto_20240603_0850'),
        ('students', '0003_auto_20240603_0850'),
        ('result', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='current_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.studentclass', verbose_name='Sınıfı'),
        ),
        migrations.AlterField(
            model_name='result',
            name='exam_score',
            field=models.IntegerField(default=0, verbose_name='2. Sınav'),
        ),
        migrations.AlterField(
            model_name='result',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.academicsession', verbose_name='Eğitim Yılı'),
        ),
        migrations.AlterField(
            model_name='result',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student', verbose_name='Öğrenci'),
        ),
        migrations.AlterField(
            model_name='result',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.subject', verbose_name='Ders'),
        ),
        migrations.AlterField(
            model_name='result',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.academicterm', verbose_name='Dönem'),
        ),
        migrations.AlterField(
            model_name='result',
            name='test_score',
            field=models.IntegerField(default=0, verbose_name='1. Sınav'),
        ),
    ]