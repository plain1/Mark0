from django.contrib import admin
from .models import Room, Message


class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'Token_id']
    list_display_links = ['Token_id']
    
    class Meta:
        model = Room

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'content', 'created_at']
    list_display_links = ['user', 'room', 'content', 'created_at']
