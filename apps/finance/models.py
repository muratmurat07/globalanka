from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass
from apps.students.models import Student

class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Öğrenci")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, verbose_name="Eğitim Yılı")
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, verbose_name="Dönem")
    class_for = models.ForeignKey(StudentClass, on_delete=models.CASCADE, verbose_name="Kursu")
    balance_from_previous_term = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Kayıt Ücreti")
    status = models.CharField(
        max_length=20, 
        choices=[("active", "Aktif"), ("closed", "Kapandı")],
        default="active",
        verbose_name="Durum"
    )

    class Meta:
        ordering = ["student", "term"]

    def __str__(self):
        return f"{self.student}"

    def balance(self):
        payable = self.total_amount_payable()
        paid = self.total_amount_paid()
        return payable - paid

    def amount_payable(self):
        items = InvoiceItem.objects.filter(invoice=self)
        return sum(item.amount for item in items)

    def total_amount_payable(self):
        return self.balance_from_previous_term + self.amount_payable()

    def total_amount_paid(self):
        receipts = Receipt.objects.filter(invoice=self)
        return sum(receipt.amount_paid for receipt in receipts)

    def get_absolute_url(self):
        return reverse("invoice-detail", kwargs={"pk": self.pk})


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Daha doğru bir tutar formatı

    def __str__(self):
        return f"{self.description} - {self.amount}"


class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ödeme Miktarı")  # Daha doğru bir tutar formatı
    date_paid = models.DateField(default=timezone.now, verbose_name="Ödeme Tarihi")
    comment = models.CharField(max_length=200, blank=True, verbose_name="Açıklama")
    

    def __str__(self):
        return f"Receipt on {self.date_paid} - {self.amount_paid}"
    
    class Meta:
        ordering = ['-date_paid']  # Son ödemeleri en üstte listelemek için
        get_latest_by = 'date_paid'  # latest() çağrıldığında bu alanı kullanır
        