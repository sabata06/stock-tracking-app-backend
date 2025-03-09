from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sales.models import Sale
from django.db.models import Sum
from datetime import datetime
from sales.models import SaleItem
from django.db.models import F, Sum


class SalesListAnalyticsView(APIView):
    """
    GET endpoint to retrieve filtered sales analytics.

    Query parameters:
      - start_date (ISO format, e.g., 2025-03-01T00:00:00)
      - end_date (ISO format, e.g., 2025-03-31T23:59:59)
      - store_id (integer)
      - sales_rep_id (integer)
      - campaign_id (integer)

    Returns:
      - Total number of sales
      - Total sales amount
      - List of sales with basic details
    """

    def get(self, request, format=None):
        sales = Sale.objects.all()

        # Filter by start_date
        start_date = request.query_params.get("start_date")
        if start_date:
            try:
                start_date_parsed = datetime.fromisoformat(start_date)
                sales = sales.filter(created_at__gte=start_date_parsed)
            except Exception:
                return Response(
                    {"error": "Invalid start_date format. Use ISO format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Filter by end_date
        end_date = request.query_params.get("end_date")
        if end_date:
            try:
                end_date_parsed = datetime.fromisoformat(end_date)
                sales = sales.filter(created_at__lte=end_date_parsed)
            except Exception:
                return Response(
                    {"error": "Invalid end_date format. Use ISO format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Filter by store_id
        store_id = request.query_params.get("store_id")
        if store_id:
            sales = sales.filter(store__id=store_id)

        # Filter by sales_rep_id
        sales_rep_id = request.query_params.get("sales_rep_id")
        if sales_rep_id:
            sales = sales.filter(sales_rep__id=sales_rep_id)

        # Filter by campaign_id
        campaign_id = request.query_params.get("campaign_id")
        if campaign_id:
            sales = sales.filter(campaign__id=campaign_id)

        # Aggregate total sales amount
        total_amount = sales.aggregate(total=Sum("total_amount"))["total"] or 0

        # Prepare a basic sales list
        sales_list = []
        for sale in sales:
            sales_list.append(
                {
                    "id": sale.id,
                    "store": sale.store.name,
                    "sales_rep": (
                        {
                            "id": sale.sales_rep.id,
                            "first_name": sale.sales_rep.first_name,
                            "last_name": sale.sales_rep.last_name,
                        }
                        if sale.sales_rep
                        else None
                    ),
                    "total_amount": sale.total_amount,
                    "payment_type": sale.payment_type,
                    "created_at": sale.created_at,
                    "campaign": sale.campaign.name if sale.campaign else None,
                }
            )

        return Response(
            {
                "total_sales": sales.count(),
                "total_amount": total_amount,
                "sales": sales_list,
            },
            status=status.HTTP_200_OK,
        )


class SalesPersonAnalyticsView(APIView):
    """
    GET endpoint for a sales representative's report.

    URL parametresi: user_id (satış temsilcisi ID'si)
    Query parametreleri:
      - start_date (ISO format, örn: 2025-03-01T00:00:00)
      - end_date (ISO format, örn: 2025-03-31T23:59:59)

    Çıktı:
      - Sales representative's total sales count
      - Total sales amount
      - List of sales (id, store, total_amount, payment_type, created_at, campaign)
    """

    def get(self, request, user_id, format=None):
        sales = Sale.objects.filter(sales_rep__id=user_id)

        # Tarih filtrelemesi (ISO formatında bekler)
        start_date = request.query_params.get("start_date")
        if start_date:
            try:
                start_date_parsed = datetime.fromisoformat(start_date)
                sales = sales.filter(created_at__gte=start_date_parsed)
            except Exception:
                return Response(
                    {"error": "Invalid start_date format. Use ISO format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        end_date = request.query_params.get("end_date")
        if end_date:
            try:
                end_date_parsed = datetime.fromisoformat(end_date)
                sales = sales.filter(created_at__lte=end_date_parsed)
            except Exception:
                return Response(
                    {"error": "Invalid end_date format. Use ISO format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        total_sales_amount = sales.aggregate(total=Sum("total_amount"))["total"] or 0

        sales_list = []
        for sale in sales:
            sales_list.append(
                {
                    "id": sale.id,
                    "store": sale.store.name,
                    "total_amount": sale.total_amount,
                    "payment_type": sale.payment_type,
                    "created_at": sale.created_at,
                    "campaign": sale.campaign.name if sale.campaign else None,
                }
            )

        data = {
            "sales_count": sales.count(),
            "total_sales_amount": total_sales_amount,
            "sales": sales_list,
        }
        return Response(data, status=status.HTTP_200_OK)


class StoreRevenueAnalyticsView(APIView):
    """
    GET endpoint for store revenue report.

    URL parametresi: store_id (mağaza ID'si)
    Query parametreleri:
      - period: "daily", "weekly", "monthly", "yearly"
      - start_date, end_date (opsiyonel, ISO format)

    Çıktı:
      - Mağazanın seçilen periyotta toplam cirosu
    """

    def get(self, request, store_id, format=None):
        sales = Sale.objects.filter(store__id=store_id)

        # Tarih filtrelemesi
        start_date = request.query_params.get("start_date")
        if start_date:
            try:
                start_date_parsed = datetime.fromisoformat(start_date)
                sales = sales.filter(created_at__gte=start_date_parsed)
            except Exception:
                return Response(
                    {"error": "Invalid start_date format. Use ISO format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        end_date = request.query_params.get("end_date")
        if end_date:
            try:
                end_date_parsed = datetime.fromisoformat(end_date)
                sales = sales.filter(created_at__lte=end_date_parsed)
            except Exception:
                return Response(
                    {"error": "Invalid end_date format. Use ISO format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        total_revenue = sales.aggregate(total=Sum("total_amount"))["total"] or 0

        data = {
            "store_id": store_id,
            "total_revenue": total_revenue,
            "sales_count": sales.count(),
        }
        return Response(data, status=status.HTTP_200_OK)


class ProductVariantAnalyticsView(APIView):
    """
    GET endpoint to analyze product variant sales.

    Çıktı:
      - Her ürün varyantı için toplam satılan adet
    """

    def get(self, request, format=None):
        # Her satış kalemi üzerinden ürün varyantı ve satılan miktarı toplayalım
        variant_data = (
            SaleItem.objects.values("product_variant")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")
        )

        # Daha sonra ürün varyantı bilgilerini de ekleyebiliriz
        data = []
        for item in variant_data:
            data.append(
                {
                    "product_variant": item["product_variant"],
                    "total_sold": item["total_quantity"],
                }
            )
        return Response(data, status=status.HTTP_200_OK)


class CampaignAnalyticsView(APIView):
    """
    GET endpoint to analyze sales by campaign.

    Çıktı:
      - Her kampanya için toplam satılan adet ve toplam tutar
    """

    def get(self, request, format=None):
        campaign_data = (
            SaleItem.objects.filter(campaign__isnull=False)
            .values("campaign")
            .annotate(
                total_quantity=Sum("quantity"),
                total_amount=Sum(F("quantity") * F("unit_price")),
            )
            .order_by("-total_quantity")
        )

        data = []
        for item in campaign_data:
            data.append(
                {
                    "campaign": item["campaign"],
                    "total_sold": item["total_quantity"],
                    "total_sales_amount": item["total_amount"],
                }
            )
        return Response(data, status=status.HTTP_200_OK)
