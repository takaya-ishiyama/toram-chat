from email.mime import image
from tabnanny import check
from django.shortcuts import render, redirect, get_list_or_404
from hawkey import Query
from pymysql import NULL
import chatapp

from chatapp.form import *
from .models import *
from django.template import loader
from django.urls import path, include
from account.models import User
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
            id=Room.objects.get(name=name).id
            return HttpResponseRedirect(reverse('chatapp:chat_room',args=[id]))
        else:
            context['text']='同名の部屋があります。別の名前で作成してください'
            return render(request, '../templates/chatapp/newroom.html',context)

    else:
        form = RoomCreateForm()
    return render(request, '../templates/chatapp/newroom.html',context)


def my_chat_room(request):
    return render(request, '../templates/chatapp/my_chat_room.html')


def setting(request):
    return render(request, '../templates/chatapp/setting.html')


def chat(request, id):
    room_name=Room.objects.get(id=id)
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

    if request.method == 'POST' and form.is_valid():
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
        'text' : text
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

