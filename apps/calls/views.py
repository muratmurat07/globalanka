from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Call


class CallListView(ListView):
    model = Call

class CallDetailView(DetailView):
    model = Call
    template_name = "calls/call_detail.html"

class CallPrintView(DetailView):
    model = Call
    template_name = "calls/call_print.html"
    
class CallCreateView(SuccessMessageMixin, CreateView):
    model = Call
    fields = "__all__"
    success_message = "Yeni arama kaydı başarı ile eklendi"

    def get_form(self):
        """add date picker in forms"""
        form = super(CallCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_interview"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form


class CallUpdateView(SuccessMessageMixin, UpdateView):
    model = Call
    fields = "__all__"
    success_message = "Görüşme başarıyla güncellendi."

    def get_form(self):
        """add date picker in forms"""
        form = super(CallUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_interview"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form


class CallDeleteView(DeleteView):
    model = Call
    success_url = reverse_lazy("call-list")
