from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ColorViewSet,
    SizeViewSet,
    ProductVariantViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'variants', ProductVariantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
