from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "get_participants", "created_at")
    search_fields = ("participants__username",)
    filter_horizontal = ("participants",)

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = "Participants"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_room", "sender", "text", "timestamp", "is_read")
    search_fields = ("sender__username", "text")
    list_filter = ("is_read", "timestamp")