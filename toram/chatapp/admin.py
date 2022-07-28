from django.contrib import admin
from .models import Messages, Room

# Register your models here.

@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Messages)
class AdminMessage(admin.ModelAdmin):
    list_display = ('username', 'created_at')