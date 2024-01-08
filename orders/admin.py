from django.contrib import admin
from .models import Order, OrderItem ,Table

# Register your models here.

admin.site.register(Table)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone','table',
                    'status','created', 'updated']
    list_filter = [ 'created', 'updated',]
    inlines = [OrderItemInline]
