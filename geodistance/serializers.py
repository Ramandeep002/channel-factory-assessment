"""
Serializers for the geodistance app.
This module defines serializers for interacting with the Address model in the geodistance app.
"""
from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for the Address model.

    This serializer converts Address model instances to JSON and vice versa,
    allowing them to be easily serialized and deserialized for API interactions.

    Attributes:
        Meta (class): Configuration class for the serializer.
            model (class): The model class to be serialized.
            fields (list or tuple): The fields to include in the serialized output.
    """
    class Meta:
        """
        Meta options for the AddressSerializer.

        Defines the configuration options for the serializer, including the model
        to be serialized and the fields to include in the serialized output.
        """
        model = Address
        fields = '__all__'
