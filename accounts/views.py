import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib import messages

from .models import CustomUser


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Ro'yxatdan o'tgandan keyin avtomatik login qilish
            return redirect("home")  # Bosh sahifaga yo'naltirish
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


def signin_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Tizimga kirgandan keyin bosh sahifaga o'tkazish
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "signin.html")


def logout_view(request):
    logout(request)
    return redirect("signin")  # Tizimdan chiqqanda Sign In sahifasiga qaytarish