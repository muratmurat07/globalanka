from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Call(models.Model):
    STATUS = [("active", "Aktif"), ("inactive", "Pasif")]

    GENDER = [("male", "Erkek"), ("female", "Kız")]

    current_status = models.CharField(max_length=10, choices=STATUS, default="active", verbose_name = "Durum")
    firstname = models.CharField(max_length=200, verbose_name = "Adı")
    surname = models.CharField(max_length=200, verbose_name = "Soyadı")

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Girilen cep telefonu numarası doğru formatta değil!"
    )
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True, verbose_name = "Cep Telefonu"
    )
    
    gender = models.CharField(max_length=10, choices=GENDER, default="male", verbose_name = "Cinsiyeti")
    date_of_birth = models.DateField(default=timezone.now, verbose_name = "Doğum Tarihi")
    address = models.TextField(blank=True, verbose_name = "Adres")
    date_of_interview = models.DateField(default=timezone.now, verbose_name = "Görüşme Tarihi")
    other_name = models.CharField(max_length=200, blank=True, verbose_name = "Verilen Ücret")
    others = models.TextField(blank=True, verbose_name = "Açıklama")

    def __str__(self):
        return f"{self.firstname}  {self.surname} "

    def get_absolute_url(self):
        return reverse("islem-yapan-kisi-detail", kwargs={"pk": self.pk})
