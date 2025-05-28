import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f"chat_{self.chat_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']

        saved_message = await self.save_message(sender_id, self.chat_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": saved_message.text,
                "sender_id": sender_id,
                "sender_username": saved_message.sender.username,
                "timestamp": saved_message.timestamp.strftime('%H:%M')
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"],
        }))

    @database_sync_to_async
    def save_message(self, sender_id, chat_id, text):
        sender = User.objects.get(id=sender_id)
        room = ChatRoom.objects.get(id=chat_id)
        return Message.objects.create(chat_room=room, sender=sender, text=text)
