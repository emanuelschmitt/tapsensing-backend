from django.db import models
from django.contrib.auth.models import User


class BaseTrackingItem(models.Model):
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User)
    device_UDID = models.CharField(max_length=200)

    class Meta:
        abstract = True


class TouchEvent(BaseTrackingItem):
    TOUCH_DOWN = 'TOUCH_DOWN'
    TOUCH_UP = 'TOUCH_UP'

    EVENT_TYPE_CHOICES = (
        (TOUCH_DOWN, 'Touch down'),
        (TOUCH_UP, 'Touch up')
    )

    type = models.CharField(
        max_length=100,
        choices=EVENT_TYPE_CHOICES
    )
    x = models.FloatField()
    y = models.FloatField()
    grid_id = models.IntegerField()


class SensorData(BaseTrackingItem):
    type = models.CharField(max_length=100)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()


class Session(models.Model):
    SITTING = 'STATUS_STARTED'
    STANDING = 'STATUS_ENDED'
    BODYPOSTURE_CHOICES = (
        (SITTING, 'Sitting'),
        (STANDING, 'Standing')
    )

    INDEX_FINGER = 'INDEX_FINGER'
    THUMB = 'THUMB'
    TYPING_MODALITY_CHOICES = (
        (INDEX_FINGER, 'Index Finger'),
        (THUMB, 'Thumb')
    )

    body_posture = models.CharField(
        max_length=100,
        choices=BODYPOSTURE_CHOICES
    )
    typing_modality = models.CharField(
        max_length=100,
        choices=TYPING_MODALITY_CHOICES
    )

    date = models.DateField()
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('user', 'date')
