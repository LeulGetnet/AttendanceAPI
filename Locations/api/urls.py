from django.urls import include, path

from .views import (
LocationRudView,
AddLocation,
DeleteLocation
)

urlpatterns = [
    path('', LocationRudView.as_view(), name = 'location-rud'),
    path('addlocation/',AddLocation.as_view(), name = 'addlocation'),
    path('deletelocation/<int:pk>/', DeleteLocation.as_view(), name='deletelocation'),
]