from django.contrib import admin
from .models import Campaign

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign_type', 'active', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    list_filter = ('campaign_type', 'active', 'start_date', 'end_date')
