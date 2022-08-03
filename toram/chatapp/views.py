from email.mime import image
import re
from tabnanny import check
from venv import create
from attr import Factory
from django.shortcuts import render, redirect, get_list_or_404
from hawkey import Query
from pymysql import NULL
import chatapp
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from chatapp.form import *
from account.form import UserChangeForm
from .models import *
from django.template import loader
from django.urls import path, include
from account.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy


# Create your views here.

def index(request):
    context = {
    'list':Room.objects.all().order_by('-created_at') ,
    }
    return render(request, '../templates/chatapp/index.html',context)


@login_required
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
            result=Room.objects.create(name=request.POST.get('name'),image=request.FILES.get('image'), master=User.objects.get(username=request.user.username))
            id=Room.objects.get(name=name).id
            room = Room.objects.filter(name=Room.objects.get(id=id))[0]
            follow_view(request,name=room.name)
            return HttpResponseRedirect(reverse('chatapp:chat_room',args=[id]))
        else:
            context['text']='同名の部屋があります。別の名前で作成してください'
            return render(request, '../templates/chatapp/newroom.html',context)

    else:
        form = RoomCreateForm()
    return render(request, '../templates/chatapp/newroom.html',context)


def my_chat_room(request):
    username=User.objects.get(username=request.user.username)
    rooms=FollowRoom.objects.filter(user=username).order_by('-created_at')
    context={
        'rooms':rooms,
    }
    return render(request, '../templates/chatapp/my_chat_room.html',context)


def setting(request):
    form=UserChangeForm()
    if request.POST:
        if form.is_valid():
            form=UserChangeForm(request.POST)
            form.save()

    context={
        'form':form,
    }
    return render(request, '../templates/chatapp/setting.html')


def chat(request, id):
    room_name=Room.objects.get(id=id)
    username=User.objects.get(username=request.user.username)
    messageform = ChatForm(request.POST or None)
    imgform=PhotosForm(request.FILES)
    message=request.POST.get('msg')
    images=request.FILES.get('images')
    room = Room.objects.filter(name=room_name)[0]
    messages = Messages.objects.filter(room__name=room_name).order_by('-created_at') 
    template = '../templates/chatapp/chat_room.html'
    loadtemplate=loader.get_template('chatapp/chat_room.html')
        
    if request.method == 'POST':
        if messageform.is_valid() and message!=None and "sendchat" in request.POST and message!="":
            result=Messages.objects.create(username=username, msg=message, room=room,image=images)
            messages = Messages.objects.filter(room__name=room_name).order_by('-created_at')
            messageform=ChatForm()
        elif "follow" in request.POST:
            follow_view(request,name=room.name)
        elif "unfollow" in request.POST:
            unfollow_view(request,name=room.name)

    follow=FollowRoom.objects.filter(user=username,room=room).exists()
    context = {
        'msg':messages,
        'room': room,
        'messageform':messageform,
        'follow': follow,
    }
    return render(request,template,context)


def detail(request,id):
    room_name=Room.objects.get(id=id)
    form=ChangeRoomFieldsFrom()
    display={}
    room = Room.objects.filter(name=room_name)[0]
    field=Room.objects.get(name=room_name)
    roomid=field.id
    name=request.POST.get('name')
    context={}
    text=""
    template = loader.get_template('chatapp/detail.html')
    if request.POST:
        form=ChangeRoomFieldsFrom(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            if Room.objects.filter(name=name).exists()==False or field.id==Room.objects.get(name=name).id:
                field.name=form.cleaned_data['name']
                if request.POST.get('image')!="":
                    field.image=form.cleaned_data['image']
                field.detail=form.cleaned_data['detail']
                field.save()
                room = Room.objects.filter(name=field.name)[0]

            else:
                text='同名の部屋があります。別の名前で作成してください'
                room.image=request.FILES.get('image')#機能していない
                room.detail=request.POST.get('detail')
            
    context = {
        'room': room,
        'text' : text,
        'field': field
    }
    return HttpResponse(template.render(context, request))


def summary(request,id):
    room_name=Room.objects.get(id=id)
    room = Room.objects.filter(name=room_name)[0]
    template = loader.get_template('chatapp/summary.html')
    context = {
        'room': room,
    }
    return HttpResponse(template.render(context, request))



@login_required
def follow_view(request, *args, **kwargs):
    try:
        user = User.objects.get(username=request.user.username)
        room = Room.objects.get(name=kwargs['name'])
    except Room.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['name']))
    _, created = FollowRoom.objects.get_or_create(user=user, room=room)
    if (created):
        messages.success(request, '{}をマイルームに追加しました'.format(room.name))
    else:
        messages.warning(request, 'あなたはすでに{}をマイルームに追加しています'.format(room.name))


"""フォロー解除"""
@login_required
def unfollow_view(request, *args, **kwargs):
    try:
        user = User.objects.get(username=request.user.username)
        room = Room.objects.get(name=kwargs['name'])
        unfollow = FollowRoom.objects.get(user=user, room=room)
        unfollow.delete()
        messages.success(request, 'マイルームから{}を削除しました'.format(user.username))
    except Room.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['name']))
        return HttpResponseRedirect(reverse_lazy('chatapp:index'))

    return HttpResponseRedirect(reverse_lazy('chatapp:chat_room', kwargs={'id': room.id}))