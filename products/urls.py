from django.contrib import admin
from django.urls import path
from .views import ProductFormView, ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('add/', ProductFormView.as_view(), name='add_product'),
]