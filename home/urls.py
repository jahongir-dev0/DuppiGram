from django.urls import path
from .views import *

urlpatterns = [
    path("", home_view, name="home"),
    path("update-profile/", update_profile, name="update_profile"),
    path("chat-room/<int:chat_id>/", chat_view, name="chat"),
]
