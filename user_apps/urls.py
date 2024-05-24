from django.urls import path
from . import views

urlpatterns=[
    path('',views.userRegistration,name='userregister'),

    path('userlogin/',views.loginPage,name='userlogin'),

    path('admin_view/',views.admin_view,name='admin_view'),

    path('verify/',views.verify,name='verify'),

    path('facility/',views.facility,name='facility'),

    path('user_view/',views.user_view,name='user_view'),

    path('user_update/<int:id>/',views.update,name='user_update'),

    path('user_delete/<int:id>/', views.delete, name='user_delete'),

    path('user_add_to_cart/<int:id>/', views.add_to_cart, name='useraddtocart'),

    path('user-view', views.userview, name='userview'),

    path('user_checkout-session/', views.checkout_session, name='user-create-checkout-session'),

    path('available/',views.available,name='available'),

    path('user_success/', views.success, name='usersuccess'),

    path('user_cancel/', views.cancel, name='usercancel'),

    path('logout/',views.logout_view,name='logout'),

]
