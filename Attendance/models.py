from PIL.Image import Image
from django.db import models
from Account.models import Account
from Locations.models import Locations
from django.db.models.signals import post_save
import datetime
from django.utils import timezone
# Create your models here.


class Attendance(models.Model):
    employee = models.ForeignKey(Account,  on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True)
    hasPunchIn = models.BooleanField(default = False)
    punchInTime = models.DateTimeField()
    punchOutTime = models.DateTimeField(null = True, blank = True)
    totalTimeServed = models.TimeField(null = True, blank = True)
    Note = models.TextField(null = True, blank = True)

    @property
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.punchInTime <= now

    @property
    def this_week_attendance(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.punchInTime <= now
    
    @property
    def this_month_attendance(self):
        now = timezone.now()
        return now - datetime.timedelta(days=30) <= self.punchInTime <= now

    def __str__(self):
        return self.employee.user.username

class Attendances(models.Model):
    employee = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    attendances = models.ManyToManyField(Attendance, null=True, blank=True)

    
    def __str__(self):
        return self.employee.user.username

    @property
    def get_total_time(self):
          
        if self.attendances:
            
            return sum([int(str(attendance.totalTimeServed).split(':')[0]) for attendance in self.attendances.all()])
        return 0

def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile=Attendances.objects.get_or_create(employee=kwargs['instance'])
post_save.connect(create_profile,sender=Account)

class DumyAttendance(models.Model):
    employee = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True)
    hasPunchIn = models.BooleanField(default = False)
    punchInTime = models.DateTimeField(auto_now=True)
    Note = models.TextField(null = True, blank = True)
    def __str__(self):
        return self.employee.user.username

class PostMethod(models.Model):
   
    Image = models.ImageField(upload_to="Account/Dummy/" , null=False , blank=False)
    Note = models.TextField(null = True, blank = True)

    def __str__(self) -> str:
        return super().__str__()