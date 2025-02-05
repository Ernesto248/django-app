from django.contrib import admin

from products.models import Product

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'price', 'created_at', 'updated_at')
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)
