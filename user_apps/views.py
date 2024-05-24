from django.conf import settings
import stripe
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


# Create your views here.
def userRegistration(request):

    login_table=loginTable()
    userprofile=UserProfile()

    if request.method=="POST":

        userprofile.username = request.POST['username']
        userprofile.password = request.POST['password']
        userprofile.password2 = request.POST['password1']

        login_table.username = request.POST['username']
        login_table.password = request.POST['password']
        login_table.password2 = request.POST['password1']
        login_table.type = 'user'

        if request.POST['password']==request.POST['password1']:
            userprofile.save()
            login_table.save()

            messages.info(request,'Registration success')
            return redirect('userlogin')
        else:
            messages.info(request,'password is not matching')
            return redirect('userregister')


    return render(request,'user/userregister.html')

def loginPage(request):

    if request.method=="POST":

        username=request.POST['username']
        password=request.POST['password']

        user=loginTable.objects.filter(username=username,password=password,type='user').exists()

        try:
            if user is not None:
                user_details=loginTable.objects.get(username=username,password=password)
                user_name=user_details.username
                type=user_details.type

                if type=='user':
                    request.session['username']=user_name
                    return redirect('user_view')
                elif type=='admin':
                     request.session['username'] = user_name
                     return redirect('admin_view')
            else:
                messages.error(request,'invalid username or password')

        except:
            messages.error(request,'invalid role')

    return render(request,'user/userlogin.html')

def admin_view(request):

    Add = Patient.objects.all()

    if request.method =="POST":
        Name  = request.POST.get('Name')
        phone  = request.POST.get('phone')
        email  = request.POST.get ('email')
        address = request.POST.get('address')
        consulting_section = request.POST.get('consulting_section')
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

        New = Patient(Name=Name,phone=phone,email=email,address=address,consulting_section=consulting_section,consulting_time=consulting_time,appoinment_fees=appoinment_fees,persons=persons)


        New.save()

    return render(request,'user/admin_view.html',{'Add':Add})

def verify(request):
    return render(request,'user/verify.html')

def facility(request):
    return render(request,'user/facility.html')

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
        return redirect('available')
    return render(request,'user/userupdate.html',{'Add':Add})

def delete(request,id):

    Add = Patient.objects.get(id=id)

    if request.method == "POST":

        Add.delete()

        return redirect('user_view')


    return render(request,'user/userdelete.html')

def add_to_cart(request,id):
    New = Patient.objects.get(id=id)

    if New.persons >0:


        cart,created = Carts.objects.get_or_create(user=request.user)
        cart_item,item_created = CartItems.objects.get_or_create(cart=cart,New=New)
        if not item_created:
            cart_item.persons+=1
            cart_item.save()
    return redirect('userview')



def userview(request):
    cart,created = Carts.objects.get_or_create(user=request.user)
    cart_items = cart.cartitems_set.all()
    cart_item = CartItems.objects.all()
    total_price = sum(item.New.appoinment_fees * item.persons for item in cart_items)
    total_items = cart_items.count()

    context = {'cart_items':cart_items,'cart_item':cart_item,'total_price':total_price,'total_items':total_items}
    return render(request,'user/usercart.html',context)



def checkout_session(request):
    cart_items=CartItems.objects.all()

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
    cart_items =CartItems.objects.all()

    for cart_item in cart_items:
        product =cart_item.New
        if product.persons >= cart_item.persons :
            product.persons -= cart_item.persons
            product.save()
        cart_items.delete()

    return render(request,'user/usersuccess.html')

def cancel(request):
    return render(request,'cancel.html')

def available(request):
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

        New = Patient(Name=Name,phone=phone,email=email,address=address,consulting_section=consulting_section,consulting_time=consulting_time,appoinment_fees=appoinment_fees,persons=persons)

        New.save()




    return render(request,'user/available.html',{'Add':Add})

def user_view(request):

    # user_name = request.session['username']


    return render(request,'user/user_view.html')


def logout_view(request):
    logout(request)
    return redirect('userlogin')
#







