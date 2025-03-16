from django.contrib import admin
from .models import Sale, SaleItem
from stores.models import StoreInventory

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'sales_rep', 'total_amount', 'payment_type', 'created_at')
    list_filter = ('store', 'payment_type', 'created_at')
    search_fields = ('store__name', 'sales_rep__email')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        sale = form.instance
        # Her bir satış kalemi için stokları güncelleyelim:
        for item in sale.items.all():
            try:
                inventory = StoreInventory.objects.get(
                    store=sale.store,
                    product_variant=item.product_variant
                )
                if inventory.quantity >= item.quantity:
                    inventory.quantity -= item.quantity
                    inventory.save()
                else:
                    # Yetersiz stok durumunda hata verebilir veya loglayabilirsiniz
                    self.message_user(request, f"Not enough stock for {item.product_variant}", level='error')
            except StoreInventory.DoesNotExist:
                self.message_user(request, f"Inventory record not found for {item.product_variant} in store {sale.store}", level='error')
