from django.urls import path

from .views import (
    InvoiceCreateView,
    InvoiceDeleteView,
    InvoiceDetailView,
    InvoiceListView,
    InvoiceTakipView,
    InvoiceUpdateView,
    ReceiptCreateView,
    ReceiptUpdateView,
    ReceiptDetailView,
    bulk_invoice,
)

urlpatterns = [
    path("list/", InvoiceListView.as_view(), name="invoice-list"),
    path("takip/", InvoiceTakipView.as_view(), name="invoice-takip"),
    path("create/", InvoiceCreateView.as_view(), name="invoice-create"),
    path("<int:pk>", InvoiceDetailView.as_view(), name="invoice-detail"),
    path("<int:pk>/update/", InvoiceUpdateView.as_view(), name="invoice-update"),
    path("<int:pk>/delete/", InvoiceDeleteView.as_view(), name="invoice-delete"),
    path('receipt/<int:pk>/detail/', ReceiptDetailView.as_view(), name='receipt-detail'),
    path("receipt/create", ReceiptCreateView.as_view(), name="receipt-create"),
    path("receipt/<int:pk>/update/", ReceiptUpdateView.as_view(), name="receipt-update"),
    path("bulk-invoice/", bulk_invoice, name="bulk-invoice"),
]