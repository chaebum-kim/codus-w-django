from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from codus.helpers import make_path_and_rename
from board.models import Tag


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    avatar = ProcessedImageField(upload_to=make_path_and_rename, processors=[ResizeToFill(
        100, 100)], format='JPEG', options={'quality': 60}, blank=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '/media/default_avatar.png'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
