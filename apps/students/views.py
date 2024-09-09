import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from dateutil.relativedelta import relativedelta
from django.utils.translation import gettext_lazy as _
from num2words import num2words
from apps.finance.models import Invoice
from .models import Student, StudentBulkUpload


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        student = self.object
        invoices = Invoice.objects.filter(student=student)

        context["payments"] = invoices
        context["total_amount_payable"] = sum(invoice.total_amount_payable() for invoice in invoices)
        context["total_amount_paid"] = sum(invoice.total_amount_paid() for invoice in invoices)
        context["total_balance"] = context["total_amount_payable"] - context["total_amount_paid"]

        return context
    
class StudentPrintView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_print.html"

    def get_context_data(self, **kwargs):
        context = super(StudentPrintView, self).get_context_data(**kwargs)
        student = self.object
        invoices = Invoice.objects.filter(student=student)

        context["payments"] = invoices
        context["total_amount_payable"] = sum(invoice.total_amount_payable() for invoice in invoices)
        context["total_amount_paid"] = sum(invoice.total_amount_paid() for invoice in invoices)
        context["total_balance"] = context["total_amount_payable"] - context["total_amount_paid"]

        return context

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.relativedelta import relativedelta
from num2words import num2words
from apps.finance.models import Invoice
from .models import Student

class StudentSenetView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_senet.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        invoices = Invoice.objects.filter(student=student)

        total_amount_payable = sum(invoice.total_amount_payable() for invoice in invoices)
        total_amount_paid = sum(invoice.total_amount_paid() for invoice in invoices)

        context["payments"] = invoices
        context["total_amount_payable"] = total_amount_payable
        context["total_amount_paid"] = total_amount_paid
        context["total_balance"] = total_amount_payable - total_amount_paid
        
        kayit_tarihi = self.object.date_of_admission
        taksit_sayisi = self.object.other_name
        
        if taksit_sayisi > 0:
            taksit_tarihleri = [kayit_tarihi + relativedelta(months=1+i) for i in range(taksit_sayisi)]
            taksit_degeri = (total_amount_payable - total_amount_paid) / taksit_sayisi
            taksit_lira = int(taksit_degeri)  # Lira kısmı
            taksit_kurus = round((taksit_degeri - taksit_lira) * 100)  # Kuruş kısmı
            taksit_degeri_words = f"{num2words(taksit_lira, lang='tr')} Türk Lirası" + (f" {num2words(taksit_kurus, lang='tr')} Kuruş" if taksit_kurus > 0 else "")
        else:
            taksit_tarihleri = []
            taksit_degeri = 0
            taksit_degeri_words = "Sıfır Türk Lirası"
        
        context["taksit_tarihleri"] = taksit_tarihleri
        context["taksit_degeri"] = taksit_degeri
        context["taksit_degeri_words"] = taksit_degeri_words
        return context


    

class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = "__all__"
    success_message = "Yeni kayıt başarıyla oluşturuldu."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        return form


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = "__all__"
    success_message = "Kayıt başarıyla güncellendi."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['passport'].widget = widgets.FileInput()
        return form


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")


class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    success_message = "Kursiyerler başarıyla güncellendi"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "registration_number",
                "surname",
                "firstname",
                "other_names",
                "gender",
                "parent_number",
                "address",
                "current_class",
            ]
        )

        return response
