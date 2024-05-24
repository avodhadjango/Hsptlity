from django.urls import path
from . import views

urlpatterns=[
    path('',views.style,name='style'),

    path('register/',views.Register_user,name='register'),

    path('login/',views.loginUser,name='login'),

    path('logout/',views.logout,name='logout'),

    path('create/',views.homepage,name='home'),

    path('home/',views.Create,name='create'),

    path('update/<int:id>/',views.update,name='update'),

    path('delete/<int:id>/',views.delete,name='delete'),

    path('history/',views.history,name='history'),

    path('add_to_cart/<int:id>/',views.add_to_cart,name='addtocart'),

    path('view',views.view,name='view'),

    path('checkout-session/',views.checkout_session,name='create-checkout-session'),

    path('success/',views.success,name='success'),

    path('cancel/', views.cancel, name='cancel'),

    path('awareness/',views.awareness,name='awareness'),



    #

 ]