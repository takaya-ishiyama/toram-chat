from attr import field
from django import forms
from .models import *

class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name','image',)
        labels={
            'name':'部屋の名前',
            'image':'アイコン画像',
        }

class ChangeRoomFieldsFrom(forms.ModelForm):
    class Meta:
        model=Room
        fields=('name','image','detail')
        labels={
            'name':'部屋の名前',
            'image':'アイコン画像',
            'detail':'ルーム詳細',
            }
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
 
    def clean_name(self):
        name = self.cleaned_data['name']
        return name
 
    def clean_image(self):
        image = self.cleaned_data['image']
        return image
    
    def clean_master(self):
        master = self.cleaned_data['master']
        return master
    
    def clean_detail(self):
        detail = self.cleaned_data['detail']
        return detail


class ChatForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ('msg',)




class ImagesForm(forms.Form):
    photos_field = forms.ImageField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}))


class FollowRoomForm(forms.Form):
    class Meta:
        fields=()