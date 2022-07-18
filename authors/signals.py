# from django.contrib.auth import get_user_model
# the code above should be used when you customize your user model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()
