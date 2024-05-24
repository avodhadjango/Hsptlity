from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password2=models.CharField(max_length=200)


class loginTable(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password2=models.CharField(max_length=200)
    type=models.CharField(max_length=200)


class Patient(models.Model):
    Name = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    consulting_section = models.CharField(max_length=20)
    consulting_time = models.CharField(max_length=200)
    appoinment_fees = models.IntegerField()
    persons = models.IntegerField()

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(Patient)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    New = models.ForeignKey(Patient,on_delete=models.CASCADE)
    persons = models.PositiveIntegerField(default=1)
    appoinment_fees = models.PositiveIntegerField(default=1)
