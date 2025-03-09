from rest_framework import viewsets
from .models import Category, Product, Color, Size, ProductVariant
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ColorSerializer,
    SizeSerializer,
    ProductVariantSerializer,
)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ColorViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Colors.
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class SizeViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Sizes.
    """
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Product Variants.
    """
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
