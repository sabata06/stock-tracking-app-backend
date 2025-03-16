from rest_framework import serializers
from .models import Sale, SaleItem
from products.models import ProductVariant
from stores.models import StoreInventory


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = [
            "id",
            "product_variant",
            "quantity",
            "unit_price",
            "charged_quantity",
            "campaign",
        ]
        read_only_fields = ["unit_price", "charged_quantity", "campaign"]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "store",
            "sales_rep",
            "campaign",
            "total_amount",
            "payment_type",
            "created_at",
            "items",
        ]
        read_only_fields = ["total_amount", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        sale = Sale.objects.create(**validated_data)
        total = 0
        sale_items = []

        # Eğer tüm kalemler aynı kampanyadan ise, kampanya bilgisini satış düzeyinde de saklayabiliriz.
        sale_campaign = validated_data.get("campaign", None)

        for item_data in items_data:
            # İlgili ürün varyantını alıyoruz:
            product_variant = item_data["product_variant"]
            base_price = product_variant.price  # ProductVariant modelindeki fiyat
            quantity = item_data.get("quantity", 1)

            # Kampanya bilgisi: Eğer satış düzeyinde kampanya seçildiyse, o kampanyayı
            # her kaleme de uygulayacağız. Alternatif olarak, ürünün kampanyasını da kontrol edebilirsiniz.
            campaign = sale_campaign  # veya item_data.get('campaign', None)

            # Temel hesaplama: Eğer BOGO kampanyası uygulanıyorsa,
            # ödenecek adet = (quantity // 2) + (quantity % 2)
            if (
                campaign
                and campaign.campaign_type == "BOGO"
                and hasattr(campaign, "fixed_price")
            ):
                fixed_price = campaign.fixed_price
                unit_price = fixed_price
                charged_qty = (quantity // 2) + (quantity % 2)
            else:
                unit_price = base_price
                charged_qty = quantity

            line_total = unit_price * charged_qty
            total += line_total

            sale_item = SaleItem.objects.create(
                sale=sale,
                product_variant=product_variant,
                quantity=quantity,
                unit_price=unit_price,
                charged_quantity=charged_qty,
                campaign=campaign,
            )
            sale_items.append(sale_item)

        sale.total_amount = total
        sale.save()

        # Stokları güncelle: Her satış kalemi için, ilgili mağazanın stokundan satılan miktarı düş
        for item in sale_items:
            try:
                inventory = StoreInventory.objects.get(
                    store=sale.store, product_variant=item.product_variant
                )
                if inventory.quantity >= item.quantity:
                    inventory.quantity -= item.quantity
                    inventory.save()
                else:
                    raise serializers.ValidationError(
                        {
                            "stock": f"Not enough stock for {item.product_variant}. Available: {inventory.quantity}"
                        }
                    )
            except StoreInventory.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "stock": f"Inventory record not found for {item.product_variant} in store {sale.store}"
                    }
                )

        return sale
