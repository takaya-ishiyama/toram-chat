import re
from django.shortcuts import render, redirect, get_list_or_404

from .form import *
from .models import *
from django.template import loader
from django.urls import path, include
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from .form import UserCreateForm

def register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_username = form.cleaned_data["username"]
            input_icon = request.FILES.get("icon")
            input_password = form.cleaned_data["password1"]
            # ユーザーを認証する
            new_user = authenticate(username=input_username, password=input_password, icon=input_icon) 
            if new_user is not None:
                # ユーザーをログイン状態にする
                login(request, new_user)
                return redirect("chatapp:index")
    else:
        form = UserCreationForm()
    return render(request, "account/register.html", {"form": form})

