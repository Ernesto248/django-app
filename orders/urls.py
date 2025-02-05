from django.urls import path
from .views import MyOrderView, CreateProductOrderView, RemoveProductFromOrderView

urlpatterns = [
    path('my-orders/', MyOrderView.as_view(), name='my_orders'),
    path('add-product/', CreateProductOrderView.as_view(), name='add_product_order'),
    path('remove-product/<int:product_id>/', RemoveProductFromOrderView.as_view(), name='remove_product_from_order'),
]
