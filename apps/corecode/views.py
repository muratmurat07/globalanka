from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.students.models import Student
from django.db.models import Sum
from apps.finance.models import Receipt, Invoice
from django.utils.timezone import now
import locale


from .forms import (
    AcademicSessionForm,
    AcademicTermForm,
    CurrentSessionForm,
    SiteConfigForm,
    StudentClassForm,
    SubjectForm,
)
from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
)

class IndexView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "index.html"
    context_object_name = "students"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Öğrenciler için sorgu setini önceden oluşturma
        students = Student.objects.all()

        # Toplamları hesapla
        total_students = students.count()
        total_debt = sum(student.total_amount_payable() for student in students)
        total_paid = sum(student.total_amount_paid() for student in students)
        total_balance = total_debt - total_paid

        # Türkçe tarih formatı için yerel ayarları ayarla
        locale.setlocale(locale.LC_TIME, 'tr_TR')

        # Bugünün tarihini al
        today = now().date()

        # Günlük, aylık ve yıllık gelirleri hesapla
        daily_revenue = Receipt.objects.filter(date_paid=today).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        monthly_revenue = Receipt.objects.filter(date_paid__year=today.year, date_paid__month=today.month).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        yearly_revenue = Receipt.objects.filter(date_paid__year=today.year).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        total_revenue = Receipt.objects.all().aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

        # Hesaplanan verileri context'e ekle
        context['total_students'] = total_students
        context['total_debt'] = total_debt
        context['total_paid'] = total_paid
        context['total_balance'] = total_balance

        context['daily_revenue'] = daily_revenue
        context['monthly_revenue'] = monthly_revenue
        context['yearly_revenue'] = yearly_revenue
        context['total_revenue'] = total_revenue

        context['current_month'] = today.strftime("%B")  # Ay ismi Türkçe olarak
        context['current_year'] = today.year

         # Öğrenci istatistikleri
        context['active_students'] = students.filter(current_status='active').count()
        context['inactive_students'] = students.filter(current_status='inactive').count()

        # Bu ay kaydolan öğrenci sayısı
        current_month = today.month
        current_year = today.year
        students_registered_this_month = students.filter(date_of_admission__year=current_year, date_of_admission__month=current_month).count()

        # Bu ay kaydolan öğrenci sayısını context'e ekle
        context['students_registered_this_month'] = students_registered_this_month

        return context


class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    template_name = "corecode/siteconfig.html"

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Yapılandırmalar başarıyla güncellendi")
        context = {"formset": formset, "title": "Yapılandırma"}
        return render(request, self.template_name, context)


class SessionListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSessionForm()
        return context


class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "Yeni eğitim yılı başarı ile eklendi."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context


class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy("sessions")
    success_message = "Eğitim yılı başarı ile güncellendi.."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicSession.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "Bir oturumu güncel olarak ayarlamanız gerekir.")
                return redirect("session-list")
        return super().form_valid(form)


class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicSession
    success_url = reverse_lazy("sessions")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "{} oturumu tüm ekli içeriğiyle birlikte silindi"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Geçerli olarak ayarlandığından oturum silinemiyor")
            return redirect("sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)


class TermListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicTerm
    template_name = "corecode/term_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicTermForm()
        return context


class TermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("terms")
    success_message = "Yeni dönem başarı ile eklendi"


class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = reverse_lazy("terms")
    success_message = "Dönem başarı ile güncellendi."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicTerm.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "Geçerli olarak bir dönem ayarlamanız gerekir.")
                return redirect("term")
        return super().form_valid(form)


class TermDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicTerm
    success_url = reverse_lazy("terms")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "{} terimi tüm ekli içeriğiyle birlikte silindi"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Geçerli olarak ayarlandığından dönem silinemiyor")
            return redirect("terms")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(TermDeleteView, self).delete(request, *args, **kwargs)


class ClassListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = StudentClass
    template_name = "corecode/class_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        return context


class ClassCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("classes")
    success_message = "Yeni sınıf başarı ile eklendi."


class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    fields = ["name"]
    success_url = reverse_lazy("classes")
    success_message = "Sonof başarı ile güncellendi"
    template_name = "corecode/mgt_form.html"


class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentClass
    success_url = reverse_lazy("classes")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "{} sınıfı tüm ekli içeriğiyle birlikte silindi"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.name)
        messages.success(self.request, self.success_message.format(obj.name))
        return super(ClassDeleteView, self).delete(request, *args, **kwargs)


class SubjectListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Subject
    template_name = "corecode/subject_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubjectForm()
        return context


class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("subjects")
    success_message = "Yeni ders başarı ile eklendi"


class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    fields = ["name"]
    success_url = reverse_lazy("subjects")
    success_message = "Ders başarı ile güncellendi."
    template_name = "corecode/mgt_form.html"


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("subjects")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "{} dersi, tüm ekli içeriğiyle birlikte silindi."

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SubjectDeleteView, self).delete(request, *args, **kwargs)


class CurrentSessionAndTermView(LoginRequiredMixin, View):
    """Current SEssion and Term"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            initial={
                "current_session": AcademicSession.objects.get(current=True),
                "current_term": AcademicTerm.objects.get(current=True),
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_Class(request.POST)
        if form.is_valid():
            session = form.cleaned_data["current_session"]
            term = form.cleaned_data["current_term"]
            AcademicSession.objects.filter(name=session).update(current=True)
            AcademicSession.objects.exclude(name=session).update(current=False)
            AcademicTerm.objects.filter(name=term).update(current=True)

        return render(request, self.template_name, {"form": form})
