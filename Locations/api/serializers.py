from django.db import models
from rest_framework import serializers
from Locations.models import Locations

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'
