from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='chatapp'
urlpatterns=[
    path(r'', views.index, name='index'),
    path(r'mychatroom',views.my_chat_room, name='my_chat_room'),
    path(r'setting', views.setting, name='setting'),
    path(r'chat/<room_name>',views.chat,name='chat_room'),
] 
