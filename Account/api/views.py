from datetime import date

from django.db.models.fields import NullBooleanField
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics, views, status as s
from django.contrib.auth.models import User
from Account.models import Account
from .serializers import AccountSerilizer
from django.contrib.auth import (authenticate ,get_user_model ,login , logout)
from django.contrib.auth.models import User
from rest_framework.response import Response
from Locations.models import Locations

class UserRegistrationRudview(views.APIView):
    serializer_class = AccountSerilizer

    def get_queryset(self):

        return Account.objects.all()
    
    def post(self, request, format = None):
        data = request.data
        
        username = data.get('username', None)
        email = data.get('email', None)

        if  username and User.objects.filter(username=username).exists():
            return Response({"success" : False, "err" : "sorry, username already taken"}, s.HTTP_200_OK)

        if  email and User.objects.filter(email=email).exists():
            return Response({"success" : False, "err" : "sorry, email already taken"}, s.HTTP_200_OK)
            
       
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        
        
        password = data.get('password', None)

        profile_pic = data.get('profile_pic', None)
        phone_num = data.get('phone_no', None)
        adress = data.get('address', None)

        new_user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, email = email)
        
        new_user.set_password(password)

        new_user.save()

        new_acc = Account.objects.get(user = new_user)
        new_acc.profile_pic = profile_pic
        new_acc.phone_number = phone_num
        new_acc.adress = adress
        new_acc.save()

        return Response({"success" : True}, s.HTTP_200_OK)
    


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        acc = Account.objects.get(user = user)
        token, created = Token.objects.get_or_create(user=user)
        if acc.is_approved:
            return Response({
                'token': token.key,
                'isApproved': acc.is_approved,
            })
        return Response({
                'isApproved': acc.is_approved,
            })

class CustomAdminAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        acc = Account.objects.get(user = user)
        token, created = Token.objects.get_or_create(user=user)
        if user.is_staff:
            return Response({
                'token': token.key,
                'is_superuser': user.is_superuser,
                'isApproved' : True
            })
        return Response({
                'isApproved': True,
            })

class UnAprovedImployeeView(views.APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            acc = Account.objects.filter(is_approved = False)
            serializer = AccountSerilizer(data = acc, many = True)
            serializer.is_valid(raise_exception=False)
            return Response(serializer.data, status=s.HTTP_200_OK)

class AprovedImployeeView(views.APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            acc = Account.objects.filter(is_approved = True)
            serializer = AccountSerilizer(data = acc, many = True)
            serializer.is_valid(raise_exception=False)
            return Response(serializer.data, status=s.HTTP_200_OK)
           
class DeleteAccountView(views.APIView):
    
    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser:
            _pk = kwargs['pk']
            delete_acc = Account.objects.get(pk = _pk)
            user = delete_acc.user
            if user.is_superuser:
                return Response({"success" : False, "err": "sorry you can't delete a superuser"}, s.HTTP_200_OK)
            if delete_acc:
                delete_acc.delete()
                user.delete()
                return Response({"success" : True}, s.HTTP_200_OK)
            return Response({"success" : False}, s.HTTP_200_OK)


class AproveView(views.APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            pk = kwargs['pk']
            acc = Account.objects.get(pk = pk)
            if acc:
                acc.is_approved = True
                acc.save()
                print("Aproved")
                return Response( s.HTTP_200_OK)
            return Response({"success" : False}, s.HTTP_200_OK)

        

class AssignLocationToAstaffMember(views.APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            acc_pk = kwargs['pk']
            location_id = kwargs['id']
            acc = Account.objects.get(pk = acc_pk)
            location = Locations.objects.get(pk = location_id)

            if acc.user.is_superuser:
                return Response({"success" : True, "data" : "sorry the user you selected is already superadmin"}, s.HTTP_200_OK)

            if acc.location:
                acc.location = None

            if not acc.user.is_staff:
                acc.user.is_staff = True
                acc.user.save()

            acc.location = location
            acc.save()
            return Response({"success" : True}, s.HTTP_200_OK)
        return Response({"success" : False}, s.HTTP_200_OK)


class AccountRudView(generics.ListAPIView):
    serializer_class = AccountSerilizer
    def get_queryset(self):
        return Account.objects.all()

