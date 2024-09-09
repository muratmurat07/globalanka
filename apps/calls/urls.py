from django.urls import path

from .views import (
    CallCreateView,
    CallDeleteView,
    CallDetailView,
    CallListView,
    CallUpdateView,
    CallPrintView,
)

urlpatterns = [
    path("list/", CallListView.as_view(), name="call-list"),
    path("<int:pk>/", CallDetailView.as_view(), name="call-detail"),
    path("<int:pk>/", CallPrintView.as_view(), name="call-print"),
    path("create/", CallCreateView.as_view(), name="call-create"),
    path("<int:pk>/update/", CallUpdateView.as_view(), name="call-update"),
    path("<int:pk>/delete/", CallDeleteView.as_view(), name="call-delete"),
]
