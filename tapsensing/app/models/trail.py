from django.db import models
from django.contrib.auth.models import User


class Trail(models.Model):
    STATUS_STARTED = 'STATUS_STARTED'
    STATUS_ENDED = 'STATUS_ENDED'
    STATUS_CHOICES = (
        (STATUS_STARTED, 'Began'),
        (STATUS_ENDED, 'Ended')
    )

    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES
    )
    date = models.DateField()
    user = models.ForeignKey(User)
