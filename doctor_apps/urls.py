from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='doctorhome'),

    path('doctorhistory/',views.history,name='doctorhistory'),

    path('doctorcreate/',views.Create,name='doctorcreate'),

    path('confirm/',views.confirm,name='confirm'),

    path('medicine/',views.medicine,name='medicine'),

]