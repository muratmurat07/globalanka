from django.db import models

# Create your models here.


class SiteConfig(models.Model):
    """Site Ayarları"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class AcademicSession(models.Model):
    """Eğitim Yılı"""

    name = models.CharField(max_length=200, unique=True, verbose_name = "Eğitim Yılı")
    current = models.BooleanField(default=True, verbose_name = "Aktif Eğitim Yılı")

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicTerm(models.Model):
    """Dönem"""

    name = models.CharField(max_length=20, unique=True, verbose_name = "Dönem")
    current = models.BooleanField(default=True, verbose_name = "Aktif Dönem")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Dersler"""

    name = models.CharField(max_length=200, unique=True, verbose_name = "Ders")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    """Sınıflar"""
    
    name = models.CharField(max_length=200, unique=True, verbose_name = "Sınıf" )

    class Meta:
        verbose_name = "Sınıf"
        verbose_name_plural = "Sınıflar"
        ordering = ["name"]

    def __str__(self):
        return self.name
