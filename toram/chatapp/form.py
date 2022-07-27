from django import forms
from zmq import Message
from .models import *

class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name',)


class ChatForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ('username','msg')


