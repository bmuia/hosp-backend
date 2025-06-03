from django.contrib import admin
from .models import Hospital,CustomUser

# Register your models here.

class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name','location']

class CustomAdmin(admin.ModelAdmin):
    list_display = ['email','roles','is_staff','is_superuser','is_active','hospital']
    list_filter = ['email','hospital']

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(CustomUser, CustomAdmin)