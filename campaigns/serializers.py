from rest_framework import serializers
from .models import Campaign
from products.models import Product

class CampaignSerializer(serializers.ModelSerializer):
    # Kampanyaya dahil edilecek ürünleri ID listesi olarak almak için:
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        source='products',
        write_only=True,
        required=False
    )
    # Okuma sırasında ürünlerin detaylarını göstermek isteyebilirsiniz:
    products = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Campaign
        fields = [
            'id',
            'name',
            'description',
            'campaign_type',
            'min_purchase_amount',
            'discount_amount',
            'product_ids',  # Yazma sırasında kullanılacak
            'products',     # Okuma sırasında görüntülenecek
            'active',
            'start_date',
            'end_date',
        ]
