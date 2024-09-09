from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.students.models import Student

from .forms import InvoiceItemFormset, InvoiceReceiptFormSet, Invoices
from .models import Invoice, InvoiceItem, Receipt


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "finance/invoice_list.html"

from datetime import timedelta, timezone
class InvoiceTakipView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "finance/invoice_takip.html"

    def is_overdue(self):
        latest_receipt = self.receipt_set.latest('date_paid')
        return timezone.now().date() > (latest_receipt.date_paid + timedelta(days=30))

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = "__all__"
    success_url = "/finance/list"

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = InvoiceItemFormset(
                self.request.POST, prefix="invoiceitem_set"
            )
        else:
            context["items"] = InvoiceItemFormset(prefix="invoiceitem_set")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["items"]
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = "finance/invoice_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        
        # İlgili fatura nesnesine ait makbuzları ve fatura kalemlerini al
        receipts = Receipt.objects.filter(invoice=self.object)
        context["receipts"] = receipts
        context["items"] = InvoiceItem.objects.filter(invoice=self.object)
        
        # Ödeme miktarlarının toplamını hesapla
        total_amount_paid = sum(receipt.amount_paid for receipt in receipts)
        context["total_amount_paid"] = total_amount_paid
        
        return context

class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    fields = ["student", "session", "term", "class_for", "balance_from_previous_term"]

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["receipts"] = InvoiceReceiptFormSet(
                self.request.POST, instance=self.object
            )
            context["items"] = InvoiceItemFormset(
                self.request.POST, instance=self.object
            )
        else:
            context["receipts"] = InvoiceReceiptFormSet(instance=self.object)
            context["items"] = InvoiceItemFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["receipts"]
        itemsformset = context["items"]
        if form.is_valid() and formset.is_valid() and itemsformset.is_valid():
            form.save()
            formset.save()
            itemsformset.save()
        return super().form_valid(form)


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("invoice-list")


class ReceiptCreateView(LoginRequiredMixin, CreateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        obj.invoice = invoice
        obj.save()
        return redirect("invoice-list")

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        context["invoice"] = invoice
        return context


class ReceiptUpdateView(LoginRequiredMixin, UpdateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")


class ReceiptDeleteView(LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy("invoice-list")


@login_required
def bulk_invoice(request):
    return render(request, "finance/bulk_invoice.html")


class ReceiptDetailView(DetailView):
    model = Invoice
    template_name = 'finance/receipt_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ReceiptDetailView, self).get_context_data(**kwargs)
        
        # İlgili fatura nesnesine ait makbuzları ve fatura kalemlerini al
        receipts = Receipt.objects.filter(invoice=self.object)
        context["receipts"] = receipts
        context["items"] = InvoiceItem.objects.filter(invoice=self.object)
        
        # Ödeme miktarlarının toplamını hesapla
        total_amount_paid = sum(receipt.amount_paid for receipt in receipts)
        context["total_amount_paid"] = total_amount_paid
        
        return context
