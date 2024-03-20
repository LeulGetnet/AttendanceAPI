from django.db import models
from rest_framework import serializers
from Account.api.serializers import AccountSerilizer
from Locations.api.serializers import LocationSerializer
from django.contrib.auth import (authenticate ,get_user_model ,login , logout)
from django.core.exceptions import ValidationError



from Attendance.models import Attendance, Attendances, PostMethod

class AttendanceSerializer(serializers.ModelSerializer):
    employee = AccountSerilizer()
    location = LocationSerializer()
    class Meta:
        model = Attendance
        fields = [
            'pk',
            'employee',
            'location',
            'hasPunchIn',
            'punchInTime',
            'punchOutTime',
            'totalTimeServed',
            'Note',
            'was_published_recently',
            'this_week_attendance',
            'this_month_attendance',

        ]



class AttendancesSerializer(serializers.ModelSerializer):
    employee = AccountSerilizer()
    attendances = AttendanceSerializer(many=True, read_only=True)

    class Meta:
        model = Attendances
        fields = [
            'pk',
            'employee',
            'attendances',
            'get_total_time'

        ]

class PostMethod(serializers.ModelSerializer):
   
    
    class Meta:
        model = PostMethod
        fields = [
            "Note"
        ]