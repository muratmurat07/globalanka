from django.urls import path
from .views import (
    IslemTipiListView, IslemTipiDetailView, IslemTipiCreateView, IslemTipiUpdateView, IslemTipiDeleteView,
    IslemListView, IslemDetailView, IslemCreateView, IslemUpdateView, IslemDeleteView,
    IslemYapanKisiListView, IslemYapanKisiCreateView, IslemYapanKisiUpdateView, IslemYapanKisiDeleteView, IslemYapanKisiDetailView,
    TakipEdenKisiCreateView, TakipEdenKisiUpdateView, TakipEdenKisiDeleteView, TakipEdenKisiListView, TakipEdenKisiDetailView,
    MusteriCreateView, MusteriUpdateView, MusteriDeleteView, MusteriListView, MusteriDetailView
)

urlpatterns = [
    # Diğer URL desenleri burada olacak...

     # İşlem Tipi URL'leri
    path('islem-tipi/', IslemTipiListView.as_view(), name='islem-tipi-list'),
    path('islem-tipi/<int:pk>/', IslemTipiDetailView.as_view(), name='islem-tipi-detail'),
    path('islem-tipi/create/', IslemTipiCreateView.as_view(), name='islem-tipi-create'),
    path('islem-tipi/<int:pk>/update/', IslemTipiUpdateView.as_view(), name='islem-tipi-update'),
    path('islem-tipi/<int:pk>/delete/', IslemTipiDeleteView.as_view(), name='islem-tipi-delete'),

    # İşlem URL'leri
    path('islem/', IslemListView.as_view(), name='islem-list'),
    path('islem/<int:pk>/', IslemDetailView.as_view(), name='islem-detail'),
    path('islem/create/', IslemCreateView.as_view(), name='islem-create'),
    path('islem/<int:pk>/update/', IslemUpdateView.as_view(), name='islem-update'),
    path('islem/<int:pk>/delete/', IslemDeleteView.as_view(), name='islem-delete'),

    # İşlem Yapan Kişi URL'leri
    path('islem-yapan-kisi/', IslemYapanKisiListView.as_view(), name='islem-yapan-kisi-list'),
    path('islem-yapan-kisi/<int:pk>/', IslemYapanKisiDetailView.as_view(), name='islem-yapan-kisi-detail'),
    path('islem-yapan-kisi/create/', IslemYapanKisiCreateView.as_view(), name='islem-yapan-kisi-create'),
    path('islem-yapan-kisi/<int:pk>/update/', IslemYapanKisiUpdateView.as_view(), name='islem-yapan-kisi-update'),
    path('islem-yapan-kisi/<int:pk>/delete/', IslemYapanKisiDeleteView.as_view(), name='islem-yapan-kisi-delete'),


    # Takip Eden Kişi URL'leri
    path('takip_eden_kisi/', TakipEdenKisiListView.as_view(), name='takip-eden-kisi-list'),
    path('takip_eden_kisi/<int:pk>/', TakipEdenKisiDetailView.as_view(), name='takip-eden-kisi-detail'),
    path('takip-eden-kisi/create/', TakipEdenKisiCreateView.as_view(), name='takip-eden-kisi-create'),
    path('takip-eden-kisi/<int:pk>/update/', TakipEdenKisiUpdateView.as_view(), name='takip-eden-kisi-update'),
    path('takip-eden-kisi/<int:pk>/delete/', TakipEdenKisiDeleteView.as_view(), name='takip-eden-kisi-delete'),

    # Müşteri URL'leri
    path('musteri/', MusteriListView.as_view(), name='musteri-list'),
    path('musteri/<int:pk>/', MusteriDetailView.as_view(), name='musteri-detail'),
    path('musteri/create/', MusteriCreateView.as_view(), name='musteri-create'),
    path('musteri/<int:pk>/update/', MusteriUpdateView.as_view(), name='musteri-update'),
    path('musteri/<int:pk>/delete/', MusteriDeleteView.as_view(), name='musteri-delete'),
]
