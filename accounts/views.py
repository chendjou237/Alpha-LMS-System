from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from library.views import *
from .forms import LoginForm, RegisterForm
from .models import *


def register(response):
    if response.method == "POST":
        # form = UserCreationForm(response.POST)
        # print(form)
        roll_no = response.POST["username"]
        email = response.POST["email"]
        name = response.POST["name"]
        branch = response.POST["branch"]
        if form.is_valid():

            t = studentProfile.objects.create(
                roll_no=roll_no, email=email, name=name, branch=branch)
            t.save()
            print(t)
            form.save()
            return redirect("user_login")
        return redirect("user_login")
    else:
        form = RegisterForm()
    return render(response, "accounts/register.html", {"form": form})


def user_login(request):
    if request.method == "GET":
        context = {
            "form": LoginForm()
        }
        return render(request, 'registration/login.html', context)

    if request.method == "POST":
        # context = {
        #     "form": LoginForm(request.POST)
        # }
        roll_no = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=roll_no, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            if user.is_superuser:
                return redirect('admindashboard')
            else:
                return redirect('userdashboard')

        else:
            messages.error(request, "Invalid Credentials")
            print("Invehu")
            return redirect('user_login')


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out!")
    return redirect("login")
