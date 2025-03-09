from django.contrib import admin
from .models import Category, Product, Color, Size, ProductVariant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'category', 'brand', 'gender')
    search_fields = ('name', 'barcode')
    list_filter = ('category', 'gender')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_value')
    search_fields = ('name', 'hex_value')

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'price', 'stock_quantity')
    list_filter = ('product', 'color', 'size')
    search_fields = ('product__name',)
