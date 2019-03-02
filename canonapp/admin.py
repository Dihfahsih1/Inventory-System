from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from .forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.



admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(Complaints)
admin.site.register(StaffDetails)
admin.site.register (Salary)
admin.site.register(Spend)
admin.site.register(Sundry)




