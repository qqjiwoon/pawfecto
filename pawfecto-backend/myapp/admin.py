from django.contrib import admin
from .models import Campaign, CampaignAcceptance, Deliverable, DeliverableRequirement

admin.site.register(Campaign)
admin.site.register(CampaignAcceptance)
# admin.py
admin.site.register(Deliverable)
admin.site.register(DeliverableRequirement)
