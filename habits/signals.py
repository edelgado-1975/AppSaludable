

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Crea un perfil si el usuario es nuevo, o simplemente guarda
    el perfil existente si el usuario ya existe.
    """
    if created:
        Profile.objects.create(user=instance)
    

    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)