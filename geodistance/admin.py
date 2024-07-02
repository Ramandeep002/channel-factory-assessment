"""
Admin configuration for the geodistance app.
This module registers the Address model with the Django admin site and\
      customizes the admin interface for it.
"""
from django.contrib import admin
from .models import Address

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Address model.
    This class customizes the display, search, and filtering options for Address\
          instances in the admin interface.
    """
    list_display = ['address', 'formatted_address', 'latitude', 'longitude', 'distance_km']
    search_fields = ['address', 'formatted_address']
    list_filter = ['latitude', 'longitude']
    list_editable = ['formatted_address', 'latitude', 'longitude']
    list_per_page = 10
    list_max_show_all = 100
    list_select_related = False
    list_display_links = ['address']
