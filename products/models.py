from django.db import models

# Kategori modelimiz, ürünlerin ait olduğu kategorileri tutar.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Category name (e.g., Shoes, Bags, Clothing)")
    description = models.TextField(blank=True, help_text="Optional category description")

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# Ürün modelimiz, temel ürün bilgilerini tutar.
class Product(models.Model):
    name = models.CharField(max_length=200, help_text="Product name")
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="Unique barcode if available")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, help_text="Product category")
    description = models.TextField(blank=True, help_text="Detailed product description")
    brand = models.CharField(max_length=100, blank=True, help_text="Brand of the product")
    gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Unisex', 'Unisex')],
        default='Unisex',
        help_text="Target gender for the product"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


# Renk modelimiz
class Color(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="Color name (e.g., Red, Blue, Black)")
    hex_value = models.CharField(max_length=7, blank=True, help_text="Hex code for the color (e.g., #FF0000)")

    class Meta:
        ordering = ['name']
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.name


# Beden modelimiz
class Size(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text="Size label (e.g., S, M, L, XL or numeric for shoes)")

    class Meta:
        ordering = ['name']
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self):
        return self.name


# Ürün varyant modeli: Her ürünün, farklı renk ve beden kombinasyonlarını tutar.
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', help_text="Associated product")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, help_text="Variant color")
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, help_text="Variant size")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Unit price for this variant")
    stock_quantity = models.PositiveIntegerField(default=0, help_text="Available stock for this variant")

    class Meta:
        unique_together = ('product', 'color', 'size')
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        # İyi bir gösterim: Ürün adı - Renk - Beden
        variant_info = self.product.name
        if self.color:
            variant_info += f" - {self.color.name}"
        if self.size:
            variant_info += f" - {self.size.name}"
        return variant_info
