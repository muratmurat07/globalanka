from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Islem, IslemYapanKisi, TakipEdenKisi, Musteri, Islem_Tipi
from django.db.models import Q
from django.utils.dateparse import parse_date
from django import forms
from django import forms
import calendar
import locale

# Yerel ayarları Türkçe olarak ayarlıyoruz
locale.setlocale(locale.LC_TIME, 'tr_TR') 

class AySecimForm(forms.Form):
    # Ay isimlerini Türkçe olarak alıyoruz
    AYLAR = [(str(i), calendar.month_name[i]) for i in range(1, 13)]

    ay_secimi = forms.ChoiceField(choices=AYLAR, label='Ay Seçimi', required=True)



# İşlem Tipi Listesi
class IslemTipiListView(ListView):
    model = Islem_Tipi  # Burada doğru model kullanılmalı
    template_name = 'islemler/islem_tipi/islem_tipi_list.html'

# İşlem Tipi Detayları
class IslemTipiDetailView(DetailView):
    model = Islem_Tipi  # Burada doğru model kullanılmalı
    template_name = 'islemler/islem_tipi/islem_tipi_detail.html'

# İşlem Tipi Oluşturma
class IslemTipiCreateView(SuccessMessageMixin, CreateView):
    model = Islem_Tipi  # Burada doğru model kullanılmalı
    template_name = 'islemler/islem_tipi/islem_tipi_form.html'
    fields = '__all__'
    success_message = "Yeni işlem tipi başarıyla oluşturuldu."
    
    def get_form(self):
        form = super(IslemTipiCreateView, self).get_form()
        return form

# İşlem Tipi Güncelleme
class IslemTipiUpdateView(UpdateView):
    model = Islem_Tipi  # Burada doğru model kullanılmalı
    template_name = 'islemler/islem_tipi/islem_tipi_form.html'
    fields = '__all__'
    success_message = "İşlem tipi başarıyla güncellendi."
    success_url = reverse_lazy('islem-tipi-list')

# İşlem Tipi Silme
class IslemTipiDeleteView(DeleteView):
    model = Islem_Tipi  # Burada doğru model kullanılmalı
    template_name = 'islemler/islem_tipi/islem_tipi_confirm_delete.html'
    success_url = reverse_lazy('islem-tipi-list')



# İşlem Views
class IslemListView(ListView):
    model = Islem
    template_name = 'islemler/islem/islem_list.html'

class IslemDetailView(DetailView):
    model = Islem
    template_name = 'islemler/islem/islem_detail.html'

class IslemCreateView(SuccessMessageMixin, CreateView):
    model = Islem
    template_name = 'islemler/islem/islem_form.html'
    fields = '__all__'
    success_message = "Yeni kayıt başarıyla oluşturuldu."
    
    def get_form(self):
        form = super(IslemCreateView, self).get_form()
        return form

class IslemUpdateView(UpdateView):
    model = Islem
    template_name = 'islemler/islem/islem_form.html'
    fields = '__all__'
    success_message = "İşlem başarı ile güncelendi."
    success_url = reverse_lazy('islem-list')


class IslemDeleteView(DeleteView):
    model = Islem
    template_name = 'islemler/islem/islem_confirm_delete.html'
    success_url = reverse_lazy('islem-list')


# İşlem Yapan Kişi Views
class IslemYapanKisiListView(ListView):
    model = IslemYapanKisi
    template_name = 'islemler/islem_yapan_kisi/islem_yapan_kisi_list.html'

class IslemYapanKisiDetailView(DetailView):
    model = IslemYapanKisi
    template_name = 'islemler/islem_yapan_kisi/islem_yapan_kisi_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Formu oluştur
        form = AySecimForm(self.request.GET or None)
        context['form'] = form

        # Ay seçimi işlemlerini filtrele
        if form.is_valid():
            selected_month = form.cleaned_data.get('ay_secimi')
            if selected_month:
                # İşlem tarihlerini ay olarak filtrele
                context['islemler'] = Islem.objects.filter(
                    islem_yapan=self.object,
                    islem_tarihi__month=selected_month
                )
            else:
                # Tüm işlemleri getir
                context['islemler'] = Islem.objects.filter(islem_yapan=self.object)
        else:
            # Form geçersizse tüm işlemleri getir
            context['islemler'] = Islem.objects.filter(islem_yapan=self.object)
        
        return context
    

class IslemYapanKisiCreateView(SuccessMessageMixin, CreateView):
    model = IslemYapanKisi
    template_name = 'islemler/islem_yapan_kisi/islem_yapan_kisi_form.html'
    fields = '__all__'
    success_message = "Yeni Uzman başarı ile eklendi."
    success_url = reverse_lazy('islem-yapan-kisi-list')

class IslemYapanKisiUpdateView(SuccessMessageMixin, UpdateView):
    model = IslemYapanKisi
    template_name = 'islemler/islem_yapan_kisi/islem_yapan_kisi_form.html'
    fields = '__all__'
    success_message = "Uzman başarıyla güncellendi."
    success_url = reverse_lazy('islem-yapan-kisi-list')

class IslemYapanKisiDeleteView(DeleteView):
    model = IslemYapanKisi
    template_name = 'islemler/islem_yapan_kisi/islem_yapan_kisi_confirm_delete.html'
    success_url = reverse_lazy('islem-yapan-kisi-list')


# Takip Eden Kişi Views
class TakipEdenKisiListView(ListView):
    model = TakipEdenKisi
    template_name = 'islemler/takip_eden_kisi/takip_eden_kisi_list.html'

class TakipEdenKisiDetailView(DetailView):
    model = TakipEdenKisi
    template_name = 'islemler/takip_eden_kisi/takip_eden_kisi_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Formu oluştur
        form = AySecimForm(self.request.GET or None)
        context['form'] = form

        # Ay seçimi işlemlerini filtrele
        if form.is_valid():
            selected_month = form.cleaned_data.get('ay_secimi')
            if selected_month:
                # İşlem tarihlerini ay olarak filtrele
                context['islemler'] = Islem.objects.filter(
                    takip_eden=self.object,
                    islem_tarihi__month=selected_month
                )
            else:
                # Tüm işlemleri getir
                context['islemler'] = Islem.objects.filter(takip_eden=self.object)
        else:
            # Form geçersizse tüm işlemleri getir
            context['islemler'] = Islem.objects.filter(takip_eden=self.object)
        
        return context


class TakipEdenKisiCreateView(SuccessMessageMixin, CreateView):
    model = TakipEdenKisi
    template_name = 'islemler/takip_eden_kisi/takip_eden_kisi_form.html'
    fields = '__all__'
    success_message = "Yeni Müşteri Temsilcisi başarı ile eklendi."
    success_url = reverse_lazy('takip-eden-kisi-list')

class TakipEdenKisiUpdateView(UpdateView):
    model = TakipEdenKisi
    template_name = 'islemler/takip_eden_kisi/takip_eden_kisi_form.html'
    fields = '__all__'
    success_message = "Müşteri Temsilcisi başarıyla güncellendi."
    success_url = reverse_lazy('takip-eden-kisi-list')

class TakipEdenKisiDeleteView(DeleteView):
    model = TakipEdenKisi
    template_name = 'islemler/takip_eden_kisi/takip_eden_kisi_confirm_delete.html'
    success_url = reverse_lazy('takip-eden-kisi-list')


# Müşteri Views
class MusteriListView(ListView):
    model = Musteri
    template_name = 'islemler/musteri/musteri_list.html'

class MusteriDetailView(DetailView):
    model = Musteri
    template_name = 'islemler/musteri/musteri_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # İlişkili işlemleri ekleyin
        context['islemler'] = Islem.objects.filter(musteri=self.object)
        return context

class MusteriCreateView(CreateView):
    model = Musteri
    template_name = 'islemler/musteri/musteri_form.html'
    fields = '__all__'

class MusteriUpdateView(UpdateView):
    model = Musteri
    template_name = 'islemler/musteri/musteri_form.html'
    fields = '__all__'
    success_message = "Müşteri başarıyla güncellendi."
    success_url = reverse_lazy('musteri-list')

class MusteriDeleteView(DeleteView):
    model = Musteri
    template_name = 'islemler/musteri/musteri_confirm_delete.html'
    success_url = reverse_lazy('musteri-list')
