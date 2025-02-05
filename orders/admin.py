from django.contrib import admin
from .models import Order, OrderProduct

class OrderProductAdmin(admin.TabularInline):
    model = OrderProduct
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'user', 'is_active', 'order_date')
    inlines = [OrderProductAdmin]


admin.site.register(Order, OrderAdmin)    