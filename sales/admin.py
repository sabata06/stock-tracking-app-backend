from django.contrib import admin
from .models import Sale, SaleItem
from stores.models import StoreInventory

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1  # Varsayılan olarak 1 boş form gösterir
    readonly_fields = ('unit_price', 'charged_quantity', 'campaign')
    
    def save_model(self, request, obj, form, change):
        # Eğer unit_price boşsa, otomatik olarak ürün varyantının fiyatını atayın.
        if obj.unit_price is None:
            obj.unit_price = obj.product_variant.price
        # Eğer charged_quantity 0 ise, varsayılan olarak quantity ile eşleştirin.
        if obj.charged_quantity == 0:
            obj.charged_quantity = obj.quantity
        super().save_model(request, obj, form, change)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'sales_rep', 'total_amount', 'payment_type', 'created_at')
    list_filter = ('store', 'payment_type', 'created_at')
    search_fields = ('store__name', 'sales_rep__email')
    inlines = [SaleItemInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        sale = form.instance
        # Stok güncellemesini burada yapıyoruz
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
                    self.message_user(request, f"Not enough stock for {item.product_variant}", level='error')
            except StoreInventory.DoesNotExist:
                self.message_user(request, f"Inventory record not found for {item.product_variant} in store {sale.store}", level='error')

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product_variant', 'quantity', 'unit_price', 'charged_quantity', 'campaign')
    list_filter = ('campaign', 'product_variant')
    search_fields = ('sale__id', 'product_variant__product__name')
    # Eğer ayrı bir SaleItem yönetimi de yapmak isterseniz, save_model override'ı burada da çalışır.
    def save_model(self, request, obj, form, change):
        if obj.unit_price is None:
            obj.unit_price = obj.product_variant.price
        if obj.charged_quantity == 0:
            obj.charged_quantity = obj.quantity
        super().save_model(request, obj, form, change)
