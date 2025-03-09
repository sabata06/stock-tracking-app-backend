from django.db import models
from products.models import Product

class Campaign(models.Model):
    CAMPAIGN_TYPES = [
        ('BOGO', 'Buy One Get One Free'),
        ('THRESHOLD', 'Threshold Discount'),
    ]
    
    name = models.CharField(max_length=100, help_text="Campaign name")
    description = models.TextField(blank=True, help_text="Detailed description of the campaign")
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES, help_text="Type of campaign")
    
    # BOGO için varsayılan olarak: buy 1 get 1 free (yani ikinci ürün bedava)
    # Threshold kampanyası için: min_purchase_amount ve discount_amount bilgileri kullanılacak.
    min_purchase_amount = models.DecimalField(
        max_digits=10, decimal_places=2, 
        blank=True, null=True, 
        help_text="Minimum purchase amount required for discount (for threshold campaigns)"
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, 
        blank=True, null=True, 
        help_text="Discount applied if threshold is met (for threshold campaigns)"
    )
    
    # Kampanyanın hangi ürünlere uygulanacağını belirlemek için; 
    # ürün bazında (veya kategori bazında, isterseniz genişletebilirsiniz)
    products = models.ManyToManyField(Product, blank=True, help_text="Products applicable for this campaign")
    
    active = models.BooleanField(default=True, help_text="Whether the campaign is active")
    start_date = models.DateTimeField(blank=True, null=True, help_text="Campaign start time")
    end_date = models.DateTimeField(blank=True, null=True, help_text="Campaign end time")

    class Meta:
        ordering = ['name']
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return self.name
