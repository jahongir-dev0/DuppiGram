from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name="chat_rooms")
    created_at = models.DateTimeField(auto_now_add=True)
    is_favourite = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        usernames = list(self.participants.values_list("username", flat=True))
        return f"ChatRoom ({', '.join(usernames)})" if usernames else "ChatRoom"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def get_reply_info(self):
        if self.reply_to:
            return {
                "id": self.reply_to.id,
                "sender": self.reply_to.sender.username,
                "text": self.reply_to.text[:30]
            }
        return None

    def __str__(self):
        return f"Message from {self.sender.username}: {self.text[:30]}"

class GroupChat(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='group_images/', blank=True, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_rooms')
    is_typing = models.BooleanField(default=False)  # optional: can be computed dynamically

    def get_image_url(self):
        if self.image:
            return self.image.url
        return settings.STATIC_URL + "assets/img/groups/group-01.jpg"
