from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
 
 
class UserAdmin(UserAdmin):
    model = User
    list_display = ['username',]
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
 
admin.site.register(User, UserAdmin)