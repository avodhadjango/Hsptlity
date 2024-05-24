from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import stripe
from django.urls import reverse

# Create your views here.
from. models import *

def Register_user(request):
    if request.method=="POST":

        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('password1')

        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'This username is already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'This email already taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                user.save()
            return redirect('login')
        else:
            messages.info(request,'This password not matched')
            return redirect('register')
    return render(request,'patient/register.html')



def loginUser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Please provide correct information')

    return render(request,'patient/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def homepage(request):

    return render(request,'patient/home.html')
#
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
    return render(request,'patient/home.html',{'Add':Add})


def update(request,id):

    Add = Patient.objects.get(id=id)

    if request.method =="POST":
        Name  = request.POST.get('Name')
        phone  = request.POST.get('phone')
        email  = request.POST.get ('email')
        address = request.POST.get('address')
        consulting_section =request.POST.get('consulting_section')
        consulting_time = request.POST.get('consulting_time')
        appoinment_fees = request.POST.get('appoinment_fees')
        persons = request.POST.get('persons')

        Add.Name = Name
        Add.phone = phone
        Add.email = email
        Add.address = address
        Add.consulting_section = consulting_section
        Add.consulting_time = consulting_time
        Add.appoinment_fees = appoinment_fees
        Add.persons = persons

        Add.save()
        return redirect('/home')
    return render(request,'patient/update.html',{'Add':Add})

def delete(request,id):

    Add = Patient.objects.get(id=id)

    if request.method == "POST":

        Add.delete()

        return redirect('/home')


    return render(request,'patient/delete.html')

def history(request):
    Add = Patient.objects.all()

    return render(request,'patient/history.html',{'Add':Add})

def add_to_cart(request,id):
    New = Patient.objects.get(id=id)

    if New.persons >0:


        cart,created = Cart.objects.get_or_create(user=request.user)
        cart_item,item_created = CartItem.objects.get_or_create(cart=cart,New=New)
        if not item_created:
            cart_item.persons+=1
            cart_item.save()
    return redirect('view')




def view(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    cart_item = CartItem.objects.all()
    total_price = sum(item.New.appoinment_fees * item.persons for item in cart_items)
    total_items = cart_items.count()

    context = {'cart_items':cart_items,'cart_item':cart_item,'total_price':total_price,'total_items':total_items}
    return render(request,'patient/cart.html',context)



def checkout_session(request):
    cart_items=CartItem.objects.all()

    if cart_items:
        stripe.api_key=settings.STRIPE_SECRET_KEY

        if request.method=='POST':
            line_items=[]

            for cart_item in cart_items:
                if cart_item.New:
                    line_item={
                        'price_data':{
                            'currency':'INR',
                            'unit_amount':int(cart_item.New.appoinment_fees * 100),
                            'product_data':{
                                'name':cart_item.New.Name
                            },
                        },
                        'quantity':cart_item.persons
                    }
                    line_items.append(line_item)

            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel')),
                )

                return redirect(checkout_session.url,code=303)
def success(request):
    cart_items =CartItem.objects.all()

    for cart_item in cart_items:
        product =cart_item.New
        if product.persons >= cart_item.persons :
            product.persons -= cart_item.persons
            product.save()
        cart_items.delete()

    return render(request,'patient/success.html')

def cancel(request):
    return render(request,'cancel.html')



def awareness(request):
    return render(request,'patient/awareness.html')

def style(request):
    return render(request,'patient/style.html')