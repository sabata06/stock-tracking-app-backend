from rest_framework import viewsets
from .models import Campaign
from .serializers import CampaignSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Campaigns.
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
