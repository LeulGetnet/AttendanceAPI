from os import name
from django.urls import include, path

from .views import (
 PuncInRudView,
 AttendanceRudView,
 PunchOutView,
 AttendancesRudView,
 UserAttendanceRudView,
 ThisMonthUserAttendanceRudView,
 ThisWeekUserAttendanceRudView,
 RecentUserAttendanceRudView
)

urlpatterns = [

    path('punchin/<int:pk>/', PuncInRudView.as_view(), name = 'punchin-rud'),
    path('attendance/', AttendanceRudView.as_view(), name = 'Attendance-rud'),
    path('punchout/<int:pk>/', PunchOutView.as_view(), name = 'punchout-rud'),
    path('attendances/', AttendancesRudView.as_view(), name = 'Attendances-rud'),

    path('userattendance/<int:pk>/', UserAttendanceRudView.as_view(), name = 'user-attendance'),
    path('recent/<int:pk>/', RecentUserAttendanceRudView.as_view(), name = 'recent-rud'),
    path('thisweek/<int:pk>/', ThisWeekUserAttendanceRudView.as_view(), name = 'thisweek-rud'),
    path('thismonth/<int:pk>/', ThisMonthUserAttendanceRudView.as_view(), name = 'thismonth-rud'),



]