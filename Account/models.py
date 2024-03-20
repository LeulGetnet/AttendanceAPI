from django.db import models

# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField
import cloudinary
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from Locations.models import Locations



class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    #profile_pic = models.ImageField(upload_to="Account/profile/Image" , null=False , blank=False)
    profile_pic = CloudinaryField('image')
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    adress = models.CharField(max_length=500)
    is_approved = models.BooleanField(default=False)
    location = models.OneToOneField(Locations,on_delete = models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def is_staf(self):
        return self.user.is_staff
    @property
    def is_super_admin(self):
        return self.user.is_superuser

def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile=Account.objects.get_or_create(user=kwargs['instance'])
post_save.connect(create_profile,sender=User)

'''
@receiver(pre_delete, sender=Account)
def photo_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.profile_pic.public_id)
'''