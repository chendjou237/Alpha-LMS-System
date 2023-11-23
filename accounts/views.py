from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import studentProfile
from library.views import *



def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)  # Use your custom RegisterForm here
        if form.is_valid():
            roll_no = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            name = form.cleaned_data["name"]
            branch = form.cleaned_data["branch"]

            t = studentProfile.objects.create(
                roll_no=roll_no, email=email, name=name, branch=branch, books_borrowed_count=0,
            )
            t.save()
            form.save()

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
