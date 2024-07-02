"""
Main URL configuration for the GeoRouteAPI project.

This module includes URL patterns for the admin interface and the geodistance app.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('geodistance.urls')),
]
