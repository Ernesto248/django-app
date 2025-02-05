from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import OrderProductForm
from .models import Order, OrderProduct
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect, get_object_or_404
import logging

logger = logging.getLogger(__name__)

class MyOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/my_orders.html'
    context_object_name = 'order'
    
    def get_object(self, queryset=None):
        return Order.objects.filter(is_active=True, user=self.request.user).first()

class CreateProductOrderView(LoginRequiredMixin, CreateView):
    template_name = 'orders/create_order_product.html'
    form_class = OrderProductForm
    success_url = reverse_lazy('my_orders')

    def form_valid(self, form):
        logger.info("Processing form for adding product to order.")
        
        # Obtener o crear la orden activa
        order, _ = Order.objects.get_or_create(is_active=True, user=self.request.user)
        logger.info(f"Order retrieved or created: {order.id}, Active: {order.is_active}")

        # Obtener el ID del producto y la cantidad del formulario
        product_id = self.request.POST.get('product')
        quantity_to_add = int(self.request.POST.get('quantity', 1))

        try:
            # Verificar si el producto ya está en la orden
            existing_order_product = OrderProduct.objects.filter(order=order, product_id=product_id).first()

            if existing_order_product:
                # Si ya existe, sumar la cantidad
                existing_order_product.quantity += quantity_to_add
                existing_order_product.save()
                logger.info(f"Updated quantity for product {product_id} in order {order.id}. New quantity: {existing_order_product.quantity}")
            else:
                # Si no existe, crear un nuevo OrderProduct
                order_product = form.save(commit=False)  # No guardar aún
                order_product.order = order  # Asignar la orden
                order_product.quantity = quantity_to_add  # Asignar la cantidad
                order_product.save()  # Ahora sí guardar
                logger.info("Product added to order successfully.")

            # En lugar de llamar a super().form_valid(), redirigimos directamente
            from django.shortcuts import redirect
            return redirect(self.success_url)

        except Exception as e:
            logger.error(f"Error processing order: {str(e)}")
            raise

class RemoveProductFromOrderView(View):
    def post(self, request, product_id):
        # Obtener la orden activa del usuario
        order = Order.objects.filter(user=request.user, is_active=True).first()
        
        if order:
            # Obtener el producto de la orden
            order_product = get_object_or_404(OrderProduct, order=order, product_id=product_id)
            order_product.delete()  # Eliminar el producto de la orden
        
        return redirect('my_orders')  # Redirigir a la vista de órdenes