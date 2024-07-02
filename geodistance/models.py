"""
Models for the geodistance app.

This module defines the database models for the geodistance app, including the Address model.
"""
from django.db import models

# Create your models here.
class Address(models.Model):
    """
    Model representing an address.

    Attributes:
        address (str): The raw address input by the user.
        formatted_address (str): The formatted address as returned by the geocoding service.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
        distance_km (float): The distance in kilometers from a reference point.
    """
    address = models.CharField(max_length=255)
    formatted_address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    distance_km = models.FloatField(blank=True, null=True)

    objects = models.Manager()

    # def __str__(self):
        # """
        # Returns the string representation of the Address instance.
        # Returns the formatted address if available, otherwise returns the raw address.
        # """
    #     return self.formatted_address or self.address
