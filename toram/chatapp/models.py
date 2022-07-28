from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    image=models.ImageField(upload_to='img/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Messages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    msg = models.TextField()
    room = models.ForeignKey(
        Room,
        blank=True,
        null=True,
        related_name='room_mesages',
        on_delete=models.CASCADE
    )
    username = models.CharField(max_length=50)
    #image=models.ImageField(upload_to='img/')
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.msg

# class InMessage(models.Model):
#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     room = models.ForeignKey(
#         Messages,
#         blank=True,
#         null=True,
#         related_name='in_meesages',
#         on_delete=models.CASCADE
#     )
#     # name = models.CharField(max_length=50)
#     msg = models.TextField()
#     # created_at = models.DateTimeField(default=timezone.now)
