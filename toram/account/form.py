from django import forms
from psutil import users
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from .models import Users

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username","icon")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password','icon')
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_password(self):
        return self.initial["password"]
 
    def clean_name(self):
        username = self.cleaned_data['username']
        return username
 
    def clean_icon(self):
        icon = self.cleaned_data['icon']
        return icon
    

