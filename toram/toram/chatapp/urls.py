from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='chatapp'
urlpatterns=[
    path(r'', views.index, name='index'),
    path(r'mychatroom',views.my_chat_room, name='my_chat_room'),
    path(r'setting', views.setting, name='setting'),
    path(r'chat/<id>',views.chat,name='chat_room'),
    path(r'chat/<id>/<messageid>',views.inchat,name='in_chat_room'),    
    path(r'chat/<id>/3/detail',views.detail, name='detail'),
    path(r'chat/<id>/2/summary',views.summary,name='summary'),
    path(r'chat/newroom/',views.newroom,name="newroom"),
    path(r'chat/<id>/media/images',views.images,name="images")

] 
