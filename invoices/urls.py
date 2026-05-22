from django.urls import path
from .views import create_invoice,invoice_history,invoice_detail,download_invoice

urlpatterns = [
    path('', create_invoice, name='invoice'),

    path('history/', invoice_history, name='invoice_history'),

    path('detail/<int:id>/', invoice_detail, name='invoice_detail'),

    path('download/<int:id>/', download_invoice, name='download_invoice'),
]