from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Service, User

# Register your models here.


admin.site.register(Service)
admin.site.register(User, UserAdmin)
