from django.contrib import admin
from .models import Session, TouchEvent, SensorData


class SessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'body_posture', 'typing_modality')
    list_filter = ('user', 'date')


admin.site.register(Session, SessionAdmin)


class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'x', 'y', 'z', 'type')
    list_filter = ('user', 'timestamp')


admin.site.register(SensorData, SensorDataAdmin)


class TouchEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'x', 'y', 'type', 'grid_id', 'is_hit')
    list_filter = ('user', 'timestamp', 'type')


admin.site.register(TouchEvent, TouchEventAdmin)
