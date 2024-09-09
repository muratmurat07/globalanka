from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_UP


class IslemYapanKisi(models.Model):
    adi = models.CharField(max_length=200, verbose_name="Adı")
    soyadi = models.CharField(max_length=200, verbose_name="Soyadı")
    cep_numarasi_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Girilen cep telefonu numarası doğru formatta değil!"
    )
    cep_numarasi = models.CharField(
        validators=[cep_numarasi_regex], max_length=15, verbose_name="Cep Telefonu"
    )

    class Meta:
        verbose_name = "İşlem Yapan Kişi"
        verbose_name_plural = "İşlem Yapan Kişiler"

    def __str__(self):
        return f"{self.adi} {self.soyadi}"
    
    def get_absolute_url(self):
        return reverse("islem-yapan-kisi-list")


class TakipEdenKisi(models.Model):
    adi = models.CharField(max_length=200, verbose_name="Adı")
    soyadi = models.CharField(max_length=200, verbose_name="Soyadı")
    cep_numarasi_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Girilen cep telefonu numarası doğru formatta değil!"
    )
    cep_numarasi = models.CharField(
        validators=[cep_numarasi_regex], max_length=15, verbose_name="Cep Telefonu"
    )

    class Meta:
        ordering = ["adi",]
        verbose_name = "Takip Eden Kişi"
        verbose_name_plural = "Takip Eden Kişiler"
        

    def __str__(self):
        return f"{self.adi} {self.soyadi}"
    
    def get_absolute_url(self):
        return reverse("takip-eden-kisi-list")


class Musteri(models.Model):
    DURUM_CHOICES = [
        ("Aktif", "Aktif"),
        ("Pasif", "Pasif"),
    ]

    CINSIYET_CHOICES = [
        ("Erkek", "Erkek"),
        ("Kadın", "Kadın"),
    ]

    adi = models.CharField(max_length=200, verbose_name="Adı")
    soyadi = models.CharField(max_length=200, verbose_name="Soyadı")
    
    cep_numarasi_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Girilen cep telefonu numarası doğru formatta değil!"
    )
    cep_numarasi = models.CharField(
        validators=[cep_numarasi_regex], max_length=15, verbose_name="Cep Telefonu"
    )
    takip_eden = models.ForeignKey(TakipEdenKisi, on_delete=models.SET_NULL, null=True, verbose_name="Müşteri Temsilcisi")
    cinsiyet = models.CharField(
        max_length=10, choices=CINSIYET_CHOICES, verbose_name="Cinsiyet"
    )
    adres = models.CharField(max_length=200, verbose_name="Adres")
    aciklama = models.TextField(blank=True, verbose_name="Açıklama")
    musteri_fotografi1 = models.ImageField(upload_to="musteriler/fotograflar/", blank=True, verbose_name="Müşteri Fotoğrafı 1")
    musteri_fotografi2 = models.ImageField(upload_to="musteriler/fotograflar/", blank=True, verbose_name="Müşteri Fotoğrafı 2")
    musteri_fotografi3 = models.ImageField(upload_to="musteriler/fotograflar/", blank=True, verbose_name="Müşteri Fotoğrafı 3")
    musteri_fotografi4 = models.ImageField(upload_to="musteriler/fotograflar/", blank=True, verbose_name="Müşteri Fotoğrafı 4")
    

    class Meta:
        ordering = ["soyadi", "adi"]
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"

    def __str__(self):
        return f"{self.adi} {self.soyadi}"

    def get_absolute_url(self):
        return reverse("musteri-list")
    
    
class Islem_Tipi(models.Model):
    islem_adi = models.CharField(max_length=200, verbose_name="Adı")
    islem_maliyeti = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="İşlem Maliyeti")

    class Meta:
        verbose_name = "İşlem Tipi"
        verbose_name_plural = "İşlem Tipleri"

    def __str__(self):
        return self.islem_adi

    def get_absolute_url(self):
        return reverse("islem-tipi-list") 
    

class Islem(models.Model):
    musteri = models.ForeignKey(Musteri, on_delete=models.CASCADE, verbose_name="Müşteri")
    islem_yapan = models.ForeignKey(IslemYapanKisi, on_delete=models.CASCADE, verbose_name="Uzman")
    takip_eden = models.ForeignKey(TakipEdenKisi, on_delete=models.CASCADE, verbose_name="Müşteri Temsilcisi")
    islem_tipi = models.ForeignKey(Islem_Tipi, on_delete=models.CASCADE, verbose_name="Yapılan İşlem")
    islem_tarihi = models.DateField(default=timezone.now, verbose_name="İşlem Tarihi")
    toplam_borc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ücreti")
    
    # Yüzdelik oranlar
    islem_yapan_yuzde = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)], 
        verbose_name="İşlem Yapan Yüzdesi",
        default=30.00
    )
    takip_eden_yuzde = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)], 
        verbose_name="Müşteri Temsilcisi Yüzdesi", 
        default=20.00
)


    class Meta:
        verbose_name = "İşlem"
        verbose_name_plural = "İşlemler"

    def __str__(self):
        return f"{self.islem_tipi} - {self.musteri}"

    def islem_maliyeti(self):
        return self.islem_tipi.islem_maliyeti

    def net_islem_ucreti(self):
        return self.toplam_borc - self.islem_maliyeti()

    def islem_yapan_komisyonu(self):
        net_ucret = self.net_islem_ucreti()
        komisyon = net_ucret * (self.islem_yapan_yuzde / 100)
        return komisyon.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def takip_eden_komisyonu(self):
        net_ucret = self.net_islem_ucreti()
        komisyon = net_ucret * (self.takip_eden_yuzde / 100)
        return komisyon.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def get_absolute_url(self):
        return reverse("islem-list")

    def get_absolute_url(self):
        return reverse("islem-list")
