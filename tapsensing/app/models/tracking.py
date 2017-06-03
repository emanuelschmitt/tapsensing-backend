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

    event_type = models.CharField(
        max_length=100,
        choices=EVENT_TYPE_CHOICES
    )
    rect_id = models.IntegerField()
