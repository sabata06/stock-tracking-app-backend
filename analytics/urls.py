from django.urls import path
from .views import SalesListAnalyticsView
from .views import SalesPersonAnalyticsView
from .views import StoreRevenueAnalyticsView
from .views import ProductVariantAnalyticsView
from .views import CampaignAnalyticsView

urlpatterns = [
    path("sales/", SalesListAnalyticsView.as_view(), name="analytics-sales-list"),
    path(
        "sales/person/<int:user_id>/",
        SalesPersonAnalyticsView.as_view(),
        name="analytics-sales-person",
    ),
    path(
        "sales/store/<int:store_id>/",
        StoreRevenueAnalyticsView.as_view(),
        name="analytics-store-revenue",
    ),
    path(
        "products/",
        ProductVariantAnalyticsView.as_view(),
        name="analytics-product-variants",
    ),
    path("campaigns/", CampaignAnalyticsView.as_view(), name="analytics-campaigns"),
]
