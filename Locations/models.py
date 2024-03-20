from django.db import models

# Create your models here.
class Locations(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
 
    def __str__(self) -> str:
        return self.name