from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.core.cache import cache
from django.contrib.auth.models import User


def login_page(request):
    return render(request, "accounts/login.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("crud:index")
        else:
            print("회원정보가 존재하지 않습니다.")
            return render(request, "accounts/login.html")
    else:
        return render(request, "accounts/login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        User.objects.create_user(username, "", password)
        return redirect("crud:index")
    else:
        return render(request, "accounts/signup.html")


def user_logout(request):
    logout(request)
    return redirect("crud:index")
