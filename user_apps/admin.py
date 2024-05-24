from django.contrib import admin
from . models import UserProfile,loginTable,Patient
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(loginTable)
admin.site.register(Patient)


