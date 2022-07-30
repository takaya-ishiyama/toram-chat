from attr import field
from django import forms
from zmq import Message
from .models import *

class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name','image')
        labels={
            'name':'部屋の名前',
            'image':'アイコン画像'
        }



class ChatForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ('username','msg',)


class PhotosForm(forms.Form):
    photos_field = forms.ImageField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}))
