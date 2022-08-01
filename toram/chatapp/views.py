from email.mime import image
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
    context = {
    'list':Room.objects.all().order_by('-created_at') ,
    }
    return render(request, '../templates/chatapp/index.html',context)

def newroom(request):
    form = RoomCreateForm()
    name=request.POST.get('name')
    if request.POST:
        form=RoomCreateForm(request.POST or None, request.FILES)

    context = {
        'list':Room.objects.all().order_by('-created_at') ,
        'form':form
    }
    if request.method == 'POST' and form.is_valid():
        if Room.objects.filter(name=name).exists()==False:
            form.save()
            return HttpResponseRedirect(reverse('chatapp:chat_room', args=[name]))
        else:
            context['text']='同名の部屋があります。別の名前で作成してください'
            return render(request, '../templates/chatapp/newroom.html',context)

    else:
        form = RoomCreateForm()
    return render(request, '../templates/chatapp/newroom.html',context)


def index(request):
    form = RoomCreateForm()
    name=request.POST.get('name')
    if request.POST:
        form=RoomCreateForm(request.POST or None, request.FILES)

    context = {
        'list':Room.objects.all().order_by('-created_at') ,
        'form':form
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
    imgform=PhotosForm(request.FILES)
    username=request.POST.get('username')
    message=request.POST.get('msg')
    images=request.FILES.get('images')

    room = Room.objects.filter(name=room_name)[0]
    messages = Messages.objects.filter(room__name=room_name).order_by('-created_at') 

    template = '../templates/chatapp/chat_room.html'
    loadtemplate=loader.get_template('chatapp/chat_room.html')

    if request.method == 'POST'and form.is_valid():
        result=Messages.objects.create(username=username, msg=message, room=room,image=images)
        messages = Messages.objects.filter(room__name=room_name).order_by('-created_at')
        context = {
        'msg':messages,
        'room': room,
        }
        return HttpResponse(loadtemplate.render(context, request))
    else:
        pass

    context = {
        'msg':messages,
        'room': room,
    }
    print('-------------------------------------')
    return render(request,template,context)

def detail(request,room_name):
    form=ChangeRoomFieldsFrom()
    room = Room.objects.filter(name=room_name)[0]
    field=Room.objects.get(name=room_name)
    if request.POST:
        form=ChangeRoomFieldsFrom(request.POST, request.FILES)
    template = loader.get_template('chatapp/detail.html')

    if request.method == 'POST' and form.is_valid():
        field.name=form.cleaned_data['name']
        field.image=form.cleaned_data['image']
        field.detail=form.cleaned_data['detail']
        field.save()

    context = {
        'room': room,
        'form': form,
        'field': field
    }
    return HttpResponse(template.render(context, request))

def summary(request,room_name):
    room = Room.objects.filter(name=room_name)[0]
    template = loader.get_template('chatapp/summary.html')
    context = {
        'room': room,
    }
    return HttpResponse(template.render(context, request))

