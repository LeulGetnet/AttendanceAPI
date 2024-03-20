from django.contrib import admin

# Register your models here.
from .models import Attendance, Attendances
admin.site.register(Attendance)
admin.site.register(Attendances)