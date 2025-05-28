from django.urls import path
from .views import *

urlpatterns = [
    path("register/", signup_view, name="signup"),
    path("login/", signin_view, name="signin"),
    path("logout/", logout_view, name="logout"),
]
