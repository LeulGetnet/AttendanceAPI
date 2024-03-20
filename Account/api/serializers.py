from Locations.models import Locations
from rest_framework import serializers

from django.contrib.auth import (authenticate ,get_user_model ,login , logout)
from django.core.exceptions import ValidationError
from Account.models import Account
from Locations.api.serializers import LocationSerializer
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='email adress')
    first_name = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={
                'input_type': 'password', 'placeholder': 'Password'
               }
    )

    class Meta:
        model = User
        fields = [

            'username',
            'first_name',
            'last_name',
            'email',
            'password',

        ]


class AccountSerilizer(serializers.ModelSerializer):
    user = UserSerializer()
    location = LocationSerializer()
    class Meta:
        model = Account
        fields = [
            'pk',
            'user',
            'profile_pic',
            'phone_number',
            'adress',
            'is_staf',
            'is_super_admin',
            'is_approved',
            'location',
            ]

