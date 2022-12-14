from doctest import master
from django.db import models
from django.utils import timezone
import uuid
from account.models import User


# Create your models here.
# def images_directory_path(instance, filename):
#     return 'image-{0}/{1}'.format(instance.id, filename)

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    image=models.ImageField(upload_to='media/' ,null=True, blank=True)
    detail=models.TextField(max_length=400, null=True, blank=True)
    master=models.ForeignKey(
        User,
        related_name='room_master',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Messages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    msg = models.TextField(null=True, blank=True)
    room = models.ForeignKey(
        Room,
        related_name='room_mesages',
        on_delete=models.CASCADE
    )
    # username = models.CharField(max_length=50)
    username=models.ForeignKey(
        User,
        related_name='pmsg_user',
        on_delete=models.CASCADE,

    )
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.msg

class PMaltipleImages(models.Model):
    image=models.ImageField(upload_to='media/', null=True, blank=True)
    message=models.ForeignKey(
        Messages, 
        verbose_name="pimages",  
        on_delete=models.CASCADE
        )
    room = models.ForeignKey(
        Room,
        related_name='proom',
        on_delete=models.CASCADE
    )



class InMessages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    msg = models.TextField(null=True, blank=True)
    pmsg = models.ForeignKey(
        Messages,
        related_name='in_mesages',
        on_delete=models.CASCADE
    )
    # username = models.CharField(max_length=50)
    username=models.ForeignKey(
        User,
        related_name='smsg_user',
        on_delete=models.CASCADE,

    )
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.msg


class SMaltipleImages(models.Model):
    image=models.ImageField(upload_to='media/', null=True, blank=True)
    message=models.ForeignKey(
        InMessages, 
        verbose_name="simages",  
        on_delete=models.CASCADE
        )


class FollowRoom(models.Model):
    user=models.ForeignKey(
        User,
        related_name='user_follow_room',
        on_delete=models.CASCADE
    )
    room=models.ForeignKey(
        Room,
        related_name='followed_room_by_user',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "{} : {}".format(self.room.name, self.user.username)

class Summary(models.Model):
    primarymessage=models.ForeignKey(
        Messages,
        related_name='primary',
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    secondarymessage=models.ForeignKey(
        InMessages,
        related_name='secondary',
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    room=models.ForeignKey(
        Room,
        related_name='room',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "{}".format(self.room.name)


