from django.db import models
import uuid
from django.contrib.auth.models import PermissionsMixin, AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    icon=models.ImageField(upload_to='icon/',null=True, blank=True)
