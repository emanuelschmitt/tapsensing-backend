import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserSettings


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        logger.info('Created user settings for newly created user %s' % instance.username)
        UserSettings.objects.create(user=instance)
