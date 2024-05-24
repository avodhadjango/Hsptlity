from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from Hsptlity_apps.models import Patient


# Create your views here.

def home(request):
    return render(request,'doctor/doctorhome.html')


def history(request):
    Add = Patient.objects.all()

    return render(request,'doctor/doctorhistory.html',{'Add':Add})

def Create(request):

    Add = Patient.objects.all()

    if request.method=="POST":
        Name  = request.POST.get('Name')
        phone  = request.POST.get('phone')
        email  = request.POST.get ('email')
        address = request.POST.get('address')
        consulting_section =request.POST.get('consulting_section')
        consulting_time = request.POST.get('consulting_time')
        appoinment_fees = request.POST.get('appoinment_fees')
        persons = request.POST.get('persons')

        New = Patient(Name=Name,phone=phone,email=email,address=address,consulting_section=consulting_section,consulting_time = consulting_time ,appoinment_fees=appoinment_fees,persons=persons)

        New.save()
    return render(request,'doctor/doctorcreate.html',{'Add':Add})

def confirm(request):

    return render(request,'doctor/confirm.html')

def medicine(request):
    return render(request,'doctor/medicine.html')