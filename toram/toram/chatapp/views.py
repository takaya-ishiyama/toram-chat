from django.shortcuts import render, redirect, get_list_or_404
from pymysql import NULL
from account.views import change
import chatapp, account
import os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from chatapp.form import *
from account.form import UserChangeForm
from .models import *
from account.views import *
from django.template import loader
from django.urls import path, include
from account.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.db.models import Q


# Create your views here.

def index(request):
    results=Room.objects.none()
    text=""
    if "search" in request.POST:
        query=request.POST.get('search-room')
        query=query.split()
        for word in query:
            results = results.union(Room.objects.filter(Q(name__icontains=word)|Q(detail__icontains=word)).all())        
        if results.exists()==False:
            text="見つかりません"
        else:
            pass
    context = {
    'list':Room.objects.all().order_by('-created_at') ,
    'results':results,
    'text':text
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
            result=Room.objects.create(name=request.POST.get('name'),image=request.FILES.get('image'), master=User.objects.get(username=request.user.username), detail="")
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

@login_required
def my_chat_room(request):
    username=User.objects.get(username=request.user.username)
    rooms=FollowRoom.objects.filter(user=username).order_by('-created_at')
    context={
        'rooms':rooms,
    }
    return render(request, '../templates/chatapp/my_chat_room.html',context)

def setting(request):
    judgeprofileedit=False
    form=UserChangeForm()
    context={"judgeprofileedit":judgeprofileedit,}
    if request.method=='POST':
        if "changeprofile" in request.POST:
           context=change(request)
        if "userdelete" in request.POST:
            User.objects.filter(username=request.user.username).delete()
            logout(request)
            return index(request)
        if "profileedit" in request.POST:
            judgeprofileedit=True
            context={'form':form,
                     'judgeprofileedit':judgeprofileedit,
                    }
    template=loader.get_template('chatapp/setting.html')

    return HttpResponse(template.render(context, request))

# チャットview
def chat(request, id):
    arrow=False
    room_name=Room.objects.get(id=id)
    if request.user.is_authenticated:
        username=User.objects.get(username=request.user.username)
    else:
        username=User.objects.none()
    messageform = ChatForm(request.POST or None)
    message=request.POST.get('msg')
    images=request.FILES.getlist('images')
    room = Room.objects.filter(name=room_name)[0]
    messages = Messages.objects.filter(room__name=room_name).order_by('-created_at') 
    template = '../templates/chatapp/chat_room.html'
    loadtemplate=loader.get_template('chatapp/chat_room.html')
    

    if request.method == 'POST':
        #チャットバリテーションと登録        
        if message!=None and "sendchat" in request.POST and message!="":
            result=Messages.objects.create(username=username, msg=message, room=room)
            for l in images:
                imagesobject=PMaltipleImages.objects.create(image=l, message=result, room=room)

            messages = Messages.objects.filter(room__name=room_name).order_by('-created_at')
            messageform=ChatForm()
            roomid=str(room.id)
            return redirect('chatapp:chat_room',roomid)
        #マイルーム追加と解除
        elif "follow" in request.POST:
            follow_view(request,name=room.name)
        elif "unfollow" in request.POST:
            unfollow_view(request,name=room.name)
            
    # if request.method=='GET':
    #     if arrow==True:
    #         arrow=False
    #     else:
    #         arrow=True

        # elif "summary" in request.POST:
        #     messageobject=Messages.objects.get(id=request.POST.get('objectid'))
        #     register_summary(request, room, messageobject)

    if request.user.is_authenticated:
        follow=FollowRoom.objects.filter(user=username,room=room).exists()
    else:
        follow=False
    context = {
        'msg':messages,
        'room': room,
        'messageform':messageform,
        'follow': follow,
        'arrow':arrow,
    }
    return render(request,template,context)

# チャットinチャット
def inchat(request, id, messageid):
    displaysummary=False
    room=Room.objects.get(id=id)
    primarymessage=Messages.objects.get(id=messageid)
    summarytext=""
    already="登録済み"
    template = loader.get_template('chatapp/in_chat.html')
    if request.user.is_authenticated:
        username=User.objects.get(username=request.user.username)
    else:
        username=User.objects.none()
    messageform = ChatForm(request.POST or None, request.FILES)
    message=request.POST.get('msg')
    images=request.FILES.getlist('images')
    messages = InMessages.objects.filter(pmsg=primarymessage).order_by('-created_at') 
   
    if request.method == 'POST':
        if message!=None and "sendchat" in request.POST and message!="":
            result=InMessages.objects.create(username=username, msg=message, pmsg=primarymessage)
            for l in images:
                imagesobject=SMaltipleImages.objects.create(image=l, message=result)

            messages = InMessages.objects.filter(pmsg=primarymessage).order_by('-created_at')
            messageform=ChatForm()
            return redirect('chatapp:in_chat_room',id,str(primarymessage.id),)

        elif "psummary" in request.POST and summarytext != already:
            messageobject=Messages.objects.get(id=request.POST.get('objectid'))
            register_summary(request, room, messageobject)

        elif "ssummary" in request.POST and summarytext != already:
            messageobject=InMessages.objects.get(id=request.POST.get('objectid'))
            register_summary(request, room, messageobject)

        elif "add-summary" in request.POST:
            displaysummary=True

    context = {
        'room':room,
        'primarymessage':primarymessage,
        'msg':messages,
        'messageform':messageform,
        'displaysummary':displaysummary
    }
    return HttpResponse(template.render(context,request))

def images(request,id):
    if Messages.objects.filter(id=id).exists():
        pmobj=Messages.objects.get(id=id)
        images=pmobj.pmaltipleimages_set.all()
    elif InMessages.objects.filter(id=id).exists():
        smobj=InMessages.objects.get(id=id)
        images=smobj.smaltipleimages_set.all()

    context={'images':images,}
    return render(request,"chatapp/images.html",context)

def detail(request,id):
    all_user_display=True
    room_name=Room.objects.get(id=id)
    form=ChangeRoomFieldsFrom()
    room = Room.objects.filter(name=room_name)[0]
    field=Room.objects.get(name=room_name)
    roomid=field.id
    name=request.POST.get('name')
    context={}
    text=""
    template = loader.get_template('chatapp/detail.html')
    judge=str(request.user.username)==str(field.master)
    if request.POST:
        form=ChangeRoomFieldsFrom(request.POST, request.FILES)

    if request.method == 'POST':
        if "change" in request.POST :
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
        if "edit" in request.POST:
            edit=True
            all_user_display=False
            context = {
            'room': room,
            'text' : text,
            'edit': edit,
            'form':form,
            'all_user_display':all_user_display
            }
            return HttpResponse(template.render(context, request))
        if "roomdelete" in request.POST:
            deleteroom(request, name=room_name.name)
            return redirect('chatapp:index')

    context = {
        'room': room,
        'text' : text,
        'field': field,
        'judge': judge,
        'form':form,
        'all_user_display':all_user_display
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
        messages.success(request, '{}をマイルームから削除しました'.format(room.name))
    except Room.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['name']))
        return HttpResponseRedirect(reverse_lazy('chatapp:index'))

    return HttpResponseRedirect(reverse_lazy('chatapp:chat_room', kwargs={'id': room.id}))

@require_POST
def deleteroom(request, *args, **kwargs):
    room=Room.objects.get(name=kwargs['name'])
    room.delete()

def summary(request,id):
    room=Room.objects.get(id=id)
    summary=Summary.objects.filter(room=room)
    template = loader.get_template('chatapp/summary.html')
    if request.POST:
        if "summarydelete" in request.POST:
            delobject=request.POST.get('summaryobjectid')
            delete_summary(request, room, delobject)
            return redirect('chatapp:summary', room.id)

    context = {
        'room': room,
        'summary':summary,
    }
    return HttpResponse(template.render(context, request))


def register_summary(request, room, messageobject):
    try:
        if Messages.objects.filter(id=messageobject.id):
            pmsg=messageobject
            _, created = Summary.objects.get_or_create(primarymessage=pmsg,room=room)
        elif InMessages.objects.filter(id=messageobject.id):
            smsg=messageobject
            _, created = Summary.objects.get_or_create(secondarymessage=smsg,room=room)

    except Room.DoesNotExist:
        print('error occur')
    #     messages.warning(request, 'そのメッセージは存在しません')
    # if (created):
    #     messages.success(request, 'まとめに登録しました')
    # else:
    #     messages.warning(request, 'まとめに登録できませんでした')

@require_POST
def delete_summary(request, room, delsummary):
    try:
        if Messages.objects.filter(id=delsummary):
            obj = Summary.objects.filter(primarymessage=delsummary,room=room)
        elif InMessages.objects.filter(id=delsummary):
            obj = Summary.objects.filter(secondarymessage=delsummary,room=room)
    except Room.DoesNotExist:
        messages.warning(request, 'そのメッセージは存在しません')

    obj.delete()