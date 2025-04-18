from django.views import generic
from .forms import ProductForm
from django.urls import reverse_lazy
from .models import Product

class ProductFormView(generic.FormView):
    template_name = 'products/add_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('add_product')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ProductListView(generic.ListView):
    model = Product   
    template_name = 'products/product_list.html'
    context_object_name = 'products'