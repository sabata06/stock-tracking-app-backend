from rest_framework import serializers
from .models import Category, Product, Color, Size, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'barcode', 'category', 'category_id', 'description', 'brand', 'gender']

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_value']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']

class ProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    color = ColorSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), source='color', write_only=True, allow_null=True
    )
    size = SizeSerializer(read_only=True)
    size_id = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(), source='size', write_only=True, allow_null=True
    )
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'product_id', 'color', 'color_id', 'size', 'size_id', 'price', 'stock_quantity']
