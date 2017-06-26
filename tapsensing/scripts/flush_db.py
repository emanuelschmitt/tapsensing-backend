from app.models import SensorData, TouchEvent, Session

for s in Session.objects.all():
    s.delete()

for t in TouchEvent.objects.all():
    t.delete()

for s in SensorData.objects.all():
    s.delete()