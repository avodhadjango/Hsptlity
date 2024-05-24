from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)

class loginTable(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

class Patient(models.Model):
    Name = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    consulting_section = models.CharField(max_length=20)
    consulting_time = models.CharField(max_length=200)
    appoinment_fees = models.IntegerField()
    persons = models.IntegerField()

class Carts(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(Patient)

class CartItems(models.Model):
    cart = models.ForeignKey(Carts,on_delete=models.CASCADE)
    New = models.ForeignKey(Patient,on_delete=models.CASCADE)
    persons = models.PositiveIntegerField(default=1)
    appoinment_fees = models.PositiveIntegerField(default=1)

