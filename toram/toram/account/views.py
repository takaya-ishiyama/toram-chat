from multiprocessing import context
import re
from django.shortcuts import render, redirect, get_list_or_404
from pymysql import NULL
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .form import *
from .models import *
from django.template import loader
from django.urls import path, include
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from .form import UserCreateForm

def register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            input_username = form.cleaned_data['username']
            input_icon = request.FILES.get('icon')
            input_password = form.cleaned_data["password1"]
            # ユーザーを認証する
            new_user = authenticate(username=input_username, password=input_password) 
            if new_user is not None:
                # ユーザーをログイン状態にする
                login(request, new_user)
                return redirect("chatapp:index")
    else:
        form = UserCreateForm()
    return render(request, "account/register.html", {"form": form})

def change(request):
    user=User.objects.get(username=request.user.username)
    form=UserChangeForm(request.POST or None, request.FILES)
    if request.method == "POST" and form.is_valid():
        if not User.objects.filter(username=request.POST.get('username')).exists():
            user.username=form.cleaned_data['username']
            if request.POST.get('icon') != "":
                user.icon=form.cleaned_data['icon']

        user.save()
        context={'form':UserChangeForm(), 'user':user}
        return context

    elif request.user.username==request.POST.get('username'):
        if request.POST.get('icon') != "":
          user.icon=form.cleaned_data['icon']
        user.save()
        context={'form':UserChangeForm(), 'user':user}
        return context    
    else:
        judgeprofileedit=True
        context={'form':UserChangeForm(), 'username_already_exists':"同名のユーザーが存在します","judgeprofileedit":judgeprofileedit}
        return context

