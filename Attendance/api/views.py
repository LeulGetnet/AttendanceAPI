
from datetime import datetime
from rest_framework import generics, views, status as s
from Attendance.models import Attendance, Attendances, DumyAttendance
from .utils import face_match
from Account.models import Account
from Locations.models import Locations
from .serializers import AttendanceSerializer, AttendancesSerializer, PostMethod

from rest_framework.response import Response


class PuncInRudView(views.APIView):

    def post(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            pk = kwargs['pk']
            if pk == None:
                return Response({"data": "please select location"}, status=s.HTTP_404_NOT_FOUND)
            location = Locations.objects.get(pk = pk)
            serializer = PostMethod(data = request.data)
            serializer.is_valid()
            
            note = serializer.data.get("Note")
            #img = request.FILES["Image"].read()
            img = request.data.get("Image")           
            acc = Account.objects.get(user = request.user)
            if acc:
                if (face_match(request, img)):
                    notPunchedOutAttendance = DumyAttendance.objects.filter(employee = acc)
                    if notPunchedOutAttendance:
                        notPunchedOutAttendance.delete()
                    DumyAttendance.objects.create(employee = acc, location = location, hasPunchIn = True,  Note = note)
                    return Response({"success": True, "data" : "you have Punched in. time is: {0}".format(datetime.utcnow())}, s.HTTP_200_OK)
                            
                return Response({"success": False, "data" : "face did not mutch"}, s.HTTP_200_OK)
            return Response({"data": "no acc"}, status=s.HTTP_404_NOT_FOUND)
        return Response({"success": False},  s.HTTP_200_OK)

      
class PunchOutView(views.APIView):
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if pk == None:
            return Response({"data": "please select location"}, status=s.HTTP_404_NOT_FOUND)
        location = Locations.objects.get(pk = pk)
        acc = Account.objects.get(user = request.user)
        attendance = None
      
        if acc:
            img = request.data.get("Image")
            if (face_match(request, img)):
                        punchInAttendance, status = DumyAttendance.objects.get_or_create(employee = acc, location = location)
                  
                        attendance =  Attendance.objects.create(employee = acc, location = location, hasPunchIn = True, punchInTime = punchInAttendance.punchInTime)
     
                        now = datetime.utcnow()
      
                        if attendance.punchInTime == None:
                            punchintime = now
                        else:
                            punchintime =  attendance.punchInTime
                 
                        attendance.punchOutTime = now
                        difference =   str(now.replace(tzinfo=None) - punchintime.replace(tzinfo=None))
                        print(difference)
                        attendance.totalTimeServed = difference
  
                        attendance.save()
                   
                        listOfAtendance, stat = Attendances.objects.get_or_create(employee = acc)
                        if listOfAtendance:
        
                            listOfAtendance.attendances.add(attendance)
                      
                            listOfAtendance.save()
                           
                            punchInAttendance.delete()
                            return Response({"success": True, "data": "you have Punched Out your total time is: {0}".format(difference)}, status = s.HTTP_200_OK)

                        return Response({"success": False, "data": "You havn't Punched In yet"}, status = s.HTTP_200_OK)
            return Response({"success": False,"data": "no face match"}, status = s.HTTP_200_OK)

      
        return Response({"data": "there is no accout with that credentail"}, status=s.HTTP_404_NOT_FOUND)


            

class AttendanceRudView(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        return Attendance.objects.all()


class AttendancesRudView(views.APIView):
   
   def get(self, request):

       if request.user.is_authenticated:
            acc = Account.objects.get(user = request.user)
            attendances = Attendances.objects.filter(employee =acc)
            has_punch_in = DumyAttendance.objects.filter(employee = acc).exists()
            serializer = AttendancesSerializer(data = attendances, many = True)
            serializer.is_valid(raise_exception=False)
            serializer.data.has_punch_in = has_punch_in
            
            return Response({"data": serializer.data, "has_punch_in" :has_punch_in }, status=s.HTTP_200_OK)

       return Response({}, status = 400)

class UserAttendanceRudView(views.APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        acc = Account.objects.get(pk = pk)
        if request.user.is_staff or request.user == acc.user:
            
            if request.user.is_superuser:
                attendances = Attendance.objects.filter(employee = acc).order_by('-punchOutTime')
            else:
                admin_acc_location = Account.objects.get(user = request.user).location
                attendances = Attendance.objects.filter(employee = acc, location = admin_acc_location).order_by('-punchOutTime')

           
            serializer = AttendanceSerializer(data = attendances, many = True)
            serializer.is_valid(raise_exception=False)
            return Response(serializer.data, status=s.HTTP_200_OK)
        
        return Response({"success":True, "data" : "forbiden attempt"}, status = 403)

class RecentUserAttendanceRudView(views.APIView):

    def get(self, request,  *args, **kwargs):
        pk = kwargs['pk']
        acc = Account.objects.get(pk = pk)
       
        if request.user.is_staff or request.user == acc.user:
            
            if request.user.is_superuser:
                attendances = Attendance.objects.filter(employee = acc).order_by('-punchOutTime')
            else:
                admin_acc_location = Account.objects.get(user = request.user).Location
                attendances = Attendance.objects.filter(employee = acc, location = admin_acc_location).order_by('-punchOutTime')

            filterd = (attendance for attendance in attendances if attendance.was_published_recently )
            
            serializer = AttendanceSerializer(data = filterd, many = True)
            serializer.is_valid(raise_exception=False)
            

            return Response(serializer.data, status=s.HTTP_200_OK)
        
        return Response({"success":True, "data" : "forbiden attempt"}, status = 403)


class ThisWeekUserAttendanceRudView(views.APIView):

    def get(self, request,  *args, **kwargs):
        pk = kwargs['pk']
        acc = Account.objects.get(pk = pk)
        if request.user.is_staff or request.user == acc.user:
           
            if request.user.is_superuser:
                attendances = Attendance.objects.filter(employee = acc).order_by('-punchOutTime')
            else:
                admin_acc_location = Account.objects.get(user = request.user).Location
                attendances = Attendance.objects.filter(employee = acc, location = admin_acc_location).order_by('-punchOutTime')
            filterd = (attendance for attendance in attendances if attendance.this_week_attendance )
            
            serializer = AttendanceSerializer(data = filterd, many = True)
            serializer.is_valid(raise_exception=False)
            return Response(serializer.data, status=s.HTTP_200_OK)
        
        return Response({"success":True, "data" : "forbiden attempt"}, status = 403)


class ThisMonthUserAttendanceRudView(views.APIView):
    
    def get(self, request,  *args, **kwargs):

        pk = kwargs['pk']
        acc = Account.objects.get(pk = pk)
        
        if request.user.is_staff or request.user == acc.user:


            if request.user.is_superuser:
                attendances = Attendance.objects.filter(employee = acc).order_by('-punchOutTime')
            else:
                admin_acc_location = Account.objects.get(user = request.user).Location
                attendances = Attendance.objects.filter(employee = acc, location = admin_acc_location).order_by('-punchOutTime')
            filterd = (attendance for attendance in attendances if attendance.this_month_attendance )
            
            serializer = AttendanceSerializer(data = filterd, many = True)
            serializer.is_valid(raise_exception=False)
            return Response(serializer.data, status=s.HTTP_200_OK)
        
        return Response({"success":True, "data" : "forbiden attempt"}, status = 403)


