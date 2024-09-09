from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


from apps.corecode.models import StudentClass


class Student(models.Model):
    STATUS_CHOICES = [("active", "Aktif"), ("inactive", "Pasif")]

    GENDER_CHOICES = [("İlkokul", "İlkokul"), ("Ortaokul", "Ortaokul"), ("Lise", "Lise"), ("Üniversite", "Üniversite"), ("Yüksek Lisans", "Yüksek Lisans"), ("Doktora", "Doktora")]

    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active", verbose_name = "Durumu" 
    )
    registration_number = models.CharField(max_length=200, unique=True, verbose_name = "TC Kimlik No")
    firstname = models.CharField(max_length=200, verbose_name = "Adı")
    surname = models.CharField(max_length=200, verbose_name = "Soyadı")
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Girilen cep telefonu numarası doğru formatta değil!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True, verbose_name = "Telefon Numarası"
    )
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, default="male",verbose_name = "Öğrenim Durumu")
    date_of_birth = models.DateField(default=timezone.now, verbose_name = "Doğum Tarihi")

    date_of_admission = models.DateField(default=timezone.now, verbose_name = "Kayıt Tarihi")

    
    other_name = models.IntegerField(default=0, verbose_name="Taksit Sayısı")
    

    address = models.TextField(blank=True, verbose_name = "Adres" )
    others = models.TextField(blank=True, verbose_name = "Açıklama")
    passport = models.ImageField(blank=True, upload_to="students/passports/", verbose_name = "Öğrenci Fotoğrafı")

    class Meta:
        ordering = ["surname", "firstname", "other_name"]

    def __str__(self):
        return f"{self.firstname} {self.surname} "

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})
    
    def total_amount_payable(self):
        from apps.finance.models import Invoice  # Burada geçici import kullanıyoruz
        total = 0
        invoices = Invoice.objects.filter(student=self)
        for invoice in invoices:
            total += invoice.total_amount_payable()
        return total

    def total_amount_paid(self):
        from apps.finance.models import Invoice  # Burada geçici import kullanıyoruz
        total = 0
        invoices = Invoice.objects.filter(student=self)
        for invoice in invoices:
            total += invoice.total_amount_paid()
        return total

    def total_balance(self):
        return self.total_amount_payable() - self.total_amount_paid()
    
    


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
