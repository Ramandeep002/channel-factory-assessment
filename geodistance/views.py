"""
API views for geocoding addresses using Google Maps API.
"""
from math import radians, cos, sin, sqrt, atan2
import googlemaps
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Address
from .serializers import AddressSerializer

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

class GeocodeView(APIView):
    """
    View for geocoding addresses using Google Maps API.
    Returns serialized Address object based on the provided address parameter.
    """
    def get(self, request):
        """
        Geocode an address and return the serialized Address object.

        Parameters:
        - address (str): The address to geocode, provided as a query parameter.

        Returns:
        - JSON response with serialized Address data or error message with status code.
        """
        address = request.GET.get('address')
        if not address:
            return Response({'error': 'Address parameter is required'}, \
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            geocode_result = gmaps.geocode(address)
            if not geocode_result:
                return Response({'error': 'Failed to geocode address'}, \
                                status=status.HTTP_400_BAD_REQUEST)
            result = geocode_result[0]
            address_obj = Address.objects.create(
                address=address,
                formatted_address=result['formatted_address'],
                latitude=result['geometry']['location']['lat'],
                longitude=result['geometry']['location']['lng']
            )
            serializer = AddressSerializer(address_obj)
            return Response(serializer.data)
        except googlemaps.exceptions.HTTPError as e:
            return Response({'error': f'Google Maps API HTTP error: {str(e)}'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except googlemaps.exceptions.Timeout:
            return Response({'error': 'Google Maps API request timed out'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except googlemaps.exceptions.TransportError:
            return Response({'error': 'Network communication error with Google Maps API'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except googlemaps.exceptions.ApiError as e:
            return Response({'error': f'Google Maps API error: {str(e)}'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReverseGeocodeView(APIView):
    """
    View for reverse geocoding coordinates using Google Maps API.
    Creates and returns a serialized Address object based on the 
    provided latitude and longitude parameters.
    """
    def get(self, request):
        """
        Perform reverse geocoding and return the serialized Address object.

        Parameters:
        - lat (str): The latitude coordinate, provided as a query parameter.
        - lng (str): The longitude coordinate, provided as a query parameter.

        Returns:
        - JSON response with serialized Address data or error message with status code.
        """
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        if not lat or not lng:
            return Response({'error': 'Latitude and longitude parameters are required'}, \
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            return Response({'error': 'Invalid latitude or longitude values'}, \
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
            if not reverse_geocode_result:
                return Response({'error': 'Failed to reverse geocode'}, \
                                status=status.HTTP_400_BAD_REQUEST)
            result = reverse_geocode_result[0]
            address_obj = Address.objects.create(
                address='',
                formatted_address=result['formatted_address'],
                latitude=lat,
                longitude=lng
            )
            serializer = AddressSerializer(address_obj)
            return Response(serializer.data)
        except googlemaps.exceptions.HTTPError as e:
            return Response({'error': f'Google Maps API HTTP error: {str(e)}'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except googlemaps.exceptions.Timeout:
            return Response({'error': 'Google Maps API request timed out'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except googlemaps.exceptions.TransportError:
            return Response({'error': 'Network communication error with Google Maps API'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except googlemaps.exceptions.ApiError as e:
            return Response({'error': f'Google Maps API error: {str(e)}'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DistanceView(APIView):
    """
    View for calculating distance between two coordinates using the Haversine formula.
    Returns the distance in kilometers based on the provided latitude and longitude parameters.
    """
    def get(self, request):
        """
        Calculate distance between two coordinates and return the result.

        Parameters:
        - lat1 (str): The latitude of the first coordinate, provided as a query parameter.
        - lng1 (str): The longitude of the first coordinate, provided as a query parameter.
        - lat2 (str): The latitude of the second coordinate, provided as a query parameter.
        - lng2 (str): The longitude of the second coordinate, provided as a query parameter.

        Returns:
        - JSON response with the calculated distance in kilometers or 
        error message with status code.
        """
        lat1 = request.GET.get('lat1')
        lng1 = request.GET.get('lng1')
        lat2 = request.GET.get('lat2')
        lng2 = request.GET.get('lng2')
        try:
            lat1 = float(lat1)
            lng1 = float(lng1)
            lat2 = float(lat2)
            lng2 = float(lng2)
        except ValueError:
            return Response({'error': 'Invalid coordinate format'},\
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            # Validate latitude and longitude ranges
            if not -90 <= lat1 <= 90 or not -90 <= lat2 <= 90 or not -180 <= lng1 <= 180 \
                or not -180 <= lng2 <= 180:
                return Response({'error': 'Invalid latitude or longitude values'},\
                                status=status.HTTP_400_BAD_REQUEST)
            # Haversine formula
            earth_radius_km = 6371  # Earth radius in kilometers
            dlat = radians(lat2 - lat1)
            dlng = radians(lng2 - lng1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = earth_radius_km * c

           # Create or update the Address object
            address_obj, _ = Address.objects.update_or_create(
                address=f"{lat1},{lng1}_{lat2},{lng2}",
                defaults={
                    'formatted_address': '',
                    'latitude': None,
                    'longitude': None
                }
            )

            # Update the object with the calculated distance
            address_obj.distance_km = distance
            address_obj.save()

            serializer = AddressSerializer(address_obj)
            return Response(serializer.data)

        except ValueError:
            return Response({'error': 'Invalid coordinate format'}, \
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, \
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
