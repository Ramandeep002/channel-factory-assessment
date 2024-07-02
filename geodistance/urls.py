"""
URL configuration for the geodistance app.

This module defines URL patterns for geocoding, reverse geocoding, and distance calculation views.
"""
from django.urls import path
from .views import GeocodeView, ReverseGeocodeView, DistanceView

urlpatterns = [
    path('geocode/', GeocodeView.as_view(), name='geocode'),
    path('reverse-geocode/', ReverseGeocodeView.as_view(), name='reverse_geocode'),
    path('distance/', DistanceView.as_view(), name='distance'),
]
