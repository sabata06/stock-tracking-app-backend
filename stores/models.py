from django.db import models
from products.models import ProductVariant


class Store(models.Model):
    name = models.CharField(
        max_length=150, 
        unique=True, 
        help_text="Enter the store name."
    )
    address = models.CharField(
        max_length=255,
        help_text="Enter the full address of the store."
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Enter the contact phone number."
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Enter the contact email address."
    )
    # Coğrafi konum bilgileri (opsiyonel)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="Latitude for geolocation (optional)."
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="Longitude for geolocation (optional)."
    )
    # Durum bilgisi
    active = models.BooleanField(
        default=True,
        help_text="Designates whether this store is active."
    )
    # Zaman damgaları
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the store was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time the store was last updated."
    )

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"
        ordering = ['name']

    def __str__(self):
        return self.name

class StoreInventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('store', 'product_variant')
        verbose_name = "Store Inventory"
        verbose_name_plural = "Store Inventories"

    def __str__(self):
        return f"{self.store.name} - {self.product_variant} (qty: {self.quantity})"