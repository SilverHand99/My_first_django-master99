from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from my_projekt.models import User_Profile, Car_Complekt


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_complekt(sender, instance, created, **kwargs):
    if created:
        Car_Complekt.objects.create(user=instance)
