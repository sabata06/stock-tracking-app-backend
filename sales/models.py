from django.db import models
from django.conf import settings
from stores.models import Store
from products.models import ProductVariant
from campaigns.models import Campaign

class Sale(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, 
        help_text="Store where the sale occurred"
    )
    sales_rep = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, blank=True,
        help_text="Sales representative who made the sale"
    )
    # Opsiyonel: Eğer tüm satış kalemleri aynı kampanyadan ise, satış düzeyinde kampanya da tutulabilir.
    campaign = models.ForeignKey(
        Campaign, on_delete=models.SET_NULL, 
        null=True, blank=True,
        help_text="Campaign applied to the sale (if applicable)"
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, 
        help_text="Total sale amount"
    )
    payment_type = models.CharField(
        max_length=50,
        choices=[('cash', 'Cash'), ('credit', 'Credit'), ('other', 'Other')],
        help_text="Type of payment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="Date and time of the sale"
    )

    def __str__(self):
        rep = self.sales_rep.email if self.sales_rep else "Unknown Rep"
        return f"Sale #{self.id} at {self.store.name} by {rep}"


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name='items',
        help_text="Associated sale"
    )
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE,
        help_text="Sold product variant"
    )
    quantity = models.PositiveIntegerField(
        default=1, 
        help_text="Quantity scanned/entered"
    )
    # Sistemde otomatik olarak alınacak: ürün varyantının temel fiyatı
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, 
        help_text="Base price of the product variant", 
        editable=False
    )
    # Kampanya uygulanıyorsa (örneğin BOGO için), ücreti alınacak adet
    charged_quantity = models.PositiveIntegerField(
        default=0, 
        help_text="Effective quantity charged (computed)", 
        editable=False
    )
    # Hangi kampanyanın bu kalemde uygulandığı (varsa)
    campaign = models.ForeignKey(
        Campaign, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Campaign applied to this sale item, if any"
    )

    def __str__(self):
        return f"{self.product_variant} (x{self.quantity})"
