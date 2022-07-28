from django.shortcuts import render, redirect, get_list_or_404
from pymysql import NULL
import chatapp

from chatapp.form import *
from .models import *
from django.template import loader
from django.urls import path, include
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


# Create your views here.

# def base(request):
#     context={'username':form.objects.order_by('username')}
#     return render(request,'../templates/chatapp/base.html',context)

def index(request):
    form = RoomCreateForm(request.POST or None)
    name=request.POST.get('name')
    
    print(Room.objects.filter(name=name).exists())
    context = {
        'room_list':Room.objects.all(), 
    }
    if request.method == 'POST' and form.is_valid():
        if Room.objects.filter(name=name).exists()==False:
            form.save()
            return HttpResponseRedirect(reverse('chatapp:chat_room', args=[name]))
        else:
            context['text']='同名の部屋があります。別の名前で作成してください'
            return render(request, '../templates/chatapp/index.html',context)

    else:
        form = RoomCreateForm()
    return render(request, '../templates/chatapp/index.html',context)

def my_chat_room(request):
    return render(request, '../templates/chatapp/my_chat_room.html')


def setting(request):
    return render(request, '../templates/chatapp/setting.html')


def chat(request, room_name):
    form = ChatForm(request.POST or None)
    username=request.POST.get('username')
    message=request.POST.get('msg')
    room = Room.objects.filter(name=room_name)[0]
    messages = Messages.objects.filter(room__name=room_name).order_by('-created_at') 
    template = '../templates/chatapp/chat_room.html'
    loadtemplate=loader.get_template('chatapp/chat_room.html')

    if request.method == 'POST'and form.is_valid():
        result=Messages.objects.create(username=username, msg=message, room=room)
        print(result)
        result.save()
        messages = Messages.objects.filter(room__name=room_name).order_by('-created_at') 
        context = {
        'msg':messages,
        'room': room,
        }
        return HttpResponse(loadtemplate.render(context, request))
    else:
        form = ChatForm()

    context = {
        'msg':messages,
        'room': room,
    }
    print('-------------------------------------')
    return render(request,template,context)