from datetime import date
from django.db import models
from rest_framework import generics, views, status as s
from .serializers import LocationSerializer
from Locations.models import Locations
from rest_framework.response import Response

class LocationRudView(generics.ListAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        return Locations.objects.all().reverse()
        

class AddLocation(views.APIView):
    def post(self, request, format = None):
        if request.user.is_superuser:
            data = request.data
            name = data.get('name', None)
            location = data.get('location', None)

            if name and location:
                if name and Locations.objects.filter(name=name).exists():
                    return Response({"success" : False, "err" : "sorry, this location name is already set try anoter one"}, s.HTTP_200_OK)
                if location and Locations.objects.filter(location=location).exists():
                    return Response({"success" : False, "err" : "sorry, this location is already set"}, s.HTTP_200_OK)
                Locations.objects.create(name = name, location = location)
                return Response({"success" : True}, s.HTTP_200_OK)
            return Response({"success" : False}, s.HTTP_200_OK)


class DeleteLocation(views.APIView):
    def delete(self, request, format = None, *args, **kwargs):
        if request.user.is_superuser:
            id = kwargs['pk']
            deleted_location = Locations.objects.get(pk = id)
            if deleted_location:
                deleted_location.delete()
                return Response({"success" : True}, s.HTTP_200_OK)
            return Response({"success" : False}, s.HTTP_200_OK)


    