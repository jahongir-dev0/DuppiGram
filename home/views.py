from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.db.models.functions import Substr
import json

from .models import ChatRoom, Message, GroupChat
from accounts.models import CustomUser


@login_required
def home_view(request):
    context = get_home_context(request)
    return render(request, "index.html", context)


@login_required
def get_home_context(request):
    user = request.user
    chat_rooms = ChatRoom.objects.filter(participants=user).prefetch_related("messages")
    contacts = CustomUser.objects.exclude(id=request.user.id)
    groups = GroupChat.objects.all()
    chats = []
    for room in chat_rooms:
        other_user = room.participants.exclude(id=user.id).first()
        last_message = room.messages.last()
        unread_messages = room.messages.filter(is_read=False).exclude(sender=user).count()
        chats.append({
            "id": room.id,
            "chat_room": room,
            "other_user": other_user,
            "last_message": last_message,
            "updated_at": last_message.timestamp if last_message else room.created_at,
            "is_favourite": getattr(room, "is_favourite", False),
            "is_pinned": getattr(room, "is_pinned", False),
            "unread_messages": unread_messages,
            "avatar": other_user.get_profile_image() if other_user else "/static/assets/img/profiles/avatar-01.jpg",
            "is_online": other_user.is_online if other_user else False,
        })

    query = request.GET.get("q", "")
    contact_query = request.GET.get("contact_q", "")
    group_q = request.GET.get('group_q', '')

    if query:
        chat_rooms = chat_rooms.filter(
            participants__username__icontains=query
        )

    if contact_query:
        contacts = contacts.filter(username__icontains=contact_query)
    contacts = contacts.annotate(first_letter=Substr('username', 1, 1)).order_by('username')

    if group_q:
        groups = groups.filter(name__icontains=group_q)

    recent_chats = sorted(chats, key=lambda c: c["updated_at"], reverse=True)[:6]
    online_users = CustomUser.objects.filter(is_online=True).exclude(id=user.id)[:10]
    favourite_chats = chat_rooms.filter(is_favourite=True)

    return {
        "user": user,
        "chats": chats,
        "favourite_chats": [chat for chat in chats if chat["is_favourite"]],
        "chat_rooms": chat_rooms,
        "contacts": contacts,
        "group_chats": groups,
        "recent_chats": recent_chats,
        "online_users": online_users,
        "query": query,
        "contact_q": contact_query,
        "group_q": group_q,
        "is_active_status": user.is_online,
        "is_friends_status": user.show_friends_status,
        "today": timezone.now().date(),
    }


@login_required
def chat_view(request, chat_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_id)
    other_user = chat_room.participants.exclude(id=request.user.id).first()

    context = {
        "chat_room": chat_room,
        "other_user": other_user,
        "messages": chat_room.messages.all().order_by("timestamp")[:50],
        "emoji_list": ["02", "05", "06", "07", "08"],
    }

    context.update(get_home_context(request))
    return render(request, "chat.html", context)


@login_required
@require_POST
@csrf_exempt
def update_profile(request):
    user = request.user
    user.first_name = request.POST.get("first_name", user.first_name)
    user.last_name = request.POST.get("last_name", user.last_name)
    user.gender = request.POST.get("gender", user.gender)
    user.location = request.POST.get("about", user.location)
    user.save()
    return JsonResponse({"success": True})
