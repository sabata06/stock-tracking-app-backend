from django.contrib import admin
from .models import Sale, SaleItem

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'sales_rep', 'total_amount', 'payment_type', 'created_at')
    list_filter = ('store', 'payment_type', 'created_at')
    search_fields = ('store__name', 'sales_rep__email')

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product_variant', 'quantity', 'unit_price', 'charged_quantity', 'campaign')
    list_filter = ('campaign', 'product_variant')
    search_fields = ('sale__id', 'product_variant__product__name')

    def save_model(self, request, obj, form, change):
        # Eğer unit_price alanı boşsa, otomatik olarak ilgili ürün varyantının fiyatını kullan
        if obj.unit_price is None:
            obj.unit_price = obj.product_variant.price
        # Eğer charged_quantity değeri 0 ise, kampanya uygulanmadığı varsayılarak quantity ile eşleştir
        if obj.charged_quantity == 0:
            obj.charged_quantity = obj.quantity
        super().save_model(request, obj, form, change)
