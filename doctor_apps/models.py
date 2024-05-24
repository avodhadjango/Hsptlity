from django.db import models

# Create your models here.
class Patient(models.Model):
    Name = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    consulting_section = models.CharField(max_length=20)
    consulting_time = models.CharField(max_length=200)
    appoinment_fees = models.IntegerField()
    persons = models.IntegerField()
