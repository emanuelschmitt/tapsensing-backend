from django.contrib import admin
from .models import Session, TouchEvent, SensorData

admin.site.register(Session)
admin.site.register(SensorData)
admin.site.register(TouchEvent)
