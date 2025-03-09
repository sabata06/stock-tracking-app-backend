from rest_framework import generics
from .models import Sale
from .serializers import SaleSerializer

class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
