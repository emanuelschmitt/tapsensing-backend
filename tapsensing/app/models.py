from django.db import models
from django.contrib.auth.models import User


class UserSettings(models.Model):
    user = models.OneToOneField(User)
    lab_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class BaseTrackingItem(models.Model):
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User)
    session_code = models.CharField(max_length=100)

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
    is_hit = models.BooleanField()
    grid_shape = models.CharField(max_length=100)


class SensorData(BaseTrackingItem):
    type = models.CharField(max_length=100)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()


class Session(models.Model):
    SITTING = 'SITTING'
    STANDING = 'STANDING'
    LYING = 'LYING'
    BODYPOSTURE_CHOICES = (
        (SITTING, 'Sitting'),
        (STANDING, 'Standing'),
        (LYING, 'Lying')
    )

    INDEX_FINGER = 'INDEX'
    THUMB = 'THUMB'
    TYPING_MODALITY_CHOICES = (
        (INDEX_FINGER, 'Index Finger'),
        (THUMB, 'Thumb')
    )

    HAND_LEFT = 'HAND_LEFT'
    HAND_RIGHT = 'HAND_RIGHT'
    HAND_CHOICES = (
        (HAND_LEFT, 'Left Hand'),
        (HAND_RIGHT, 'Right Hand')
    )

    body_posture = models.CharField(
        max_length=100,
        choices=BODYPOSTURE_CHOICES
    )
    typing_modality = models.CharField(
        max_length=100,
        choices=TYPING_MODALITY_CHOICES
    )
    hand = models.CharField(
        max_length=100,
        choices=HAND_CHOICES
    )

    mood = models.CharField(max_length=100)
    date = models.DateField()
    user = models.ForeignKey(User)
    session_code = models.CharField(max_length=100)
    device_model = models.CharField(max_length=100)
    device_udid = models.CharField(max_length=100)
    lab_mode = models.BooleanField(default=False)


class PreTestSurvey(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    occupation = models.CharField(max_length=200)
    hand = models.CharField(max_length=100)

    smartphone_use = models.BooleanField()
    smartphone_model = models.CharField(max_length=200)
    input_modalities = models.CharField(max_length=200)
    most_used_input_modality = models.CharField(max_length=100)
    device_usage = models.CharField(max_length=200)
