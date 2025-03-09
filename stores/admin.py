from django.contrib import admin
from .models import Store,StoreInventory

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'active', 'created_at')
    search_fields = ('name', 'address')
    list_filter = ('active',)
    ordering = ('name',)

@admin.register(StoreInventory)
class StoreInventoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'product_variant', 'quantity')
    search_fields = ('store__name', 'product_variant__product__name')
    list_filter = ('store',)