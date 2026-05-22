from django.urls import path
from .views import product_view , add_product, delete_product, edit_product

urlpatterns = [
    path('', product_view, name='products'),
    path('add/', add_product, name='add_product'),
    path('delete/<int:id>/', delete_product, name='delete_product'),
    path('edit/<int:id>/', edit_product, name='edit_product'),    
]