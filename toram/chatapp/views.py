from django.shortcuts import render, redirect, get_list_or_404
import chatapp

from chatapp.form import *
from .models import *
from django.template import loader
from django.urls import path, include
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.

# def base(request):
#     context={'username':form.objects.order_by('username')}
#     return render(request,'../templates/chatapp/base.html',context)

def index(request):
    form = RoomCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('chatapp:index')
    else:
        form = RoomCreateForm()
    context = {
        'room_list':Room.objects.all(), 
    }
    return render(request, '../templates/chatapp/index.html',context)

def my_chat_room(request):
    return render(request, '../templates/chatapp/my_chat_room.html')

def room(request):
    name = request.POST.get("room_name")
    room = Room.objects.create(name=name)
    return HttpResponseRedirect(reverse('chatapp:chat_room', args=[name]))

def setting(request):
    return render(request, '../templates/chatapp/setting.html')

def chat(request, room_name):
    form = ChatForm(request.POST or None)
    room = Room.objects.filter(name=room_name)[0]
    template = '../templates/chatapp/chat_room.html'
    loadtemplate=loader.get_template('chatapp/chat_room.html')
    context = {
        'msg' : Messages    .objects.all(),
        'room': room,
    }
    print(context['msg'])
    print('-------------------------------------')
    # if request.method == 'POST' and form.is_valid():
    if request.method == 'POST':
        form.save()
        return HttpResponse(loadtemplate.render(context, request))
    else:
        form = ChatForm()
    return render(request,template,context)