from django.shortcuts import render, redirect
from accounts.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from accounts.models import User
from django.urls import reverse

def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect("home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            messages.success(request, f"Hello {username}, Your account is created successfully")
            return redirect("home")

    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, "accounts/sign-up.html", context)


def index(request):
    return render(request, "accounts/main.html")


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if email == "" or password == "":
            messages.warning(request, "Email and password is required") 
            return redirect("accounts:sign-in")
        else:
            try: 
                user = User.objects.get(email=email)
                
            except:
                messages.warning(request, "Email account not found")
                return redirect("accounts:sign-in")
                
            try:
                user = authenticate(request, email=email, password=password)
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("home")
            except:
                messages.warning(request, f"Password is incorrect")
                return redirect("accounts:sign-in")

    return render(request, "accounts/sign-in.html")


def logout_view(request):
    logout(request)
    messages.warning(request, "You logged out.")
    return redirect("home")


def profile_update(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user = request.user
            new_user.save()
            messages.success(request, "Profile updated successfully")
            return redirect("accounts:index")
    else:
        form = ProfileForm(instance=request.user)

    context = {
        "form": form,
        "profile": user,
    }

    return render(request, "accounts/profile-update.html", context)
