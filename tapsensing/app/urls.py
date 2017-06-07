from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views.login import login
from .views.sensordata import sensor_data
from .views.session import SessionViewSet


urls = [
    # Login
    url(r'^login/$', login),
    url(r'^sensordata/$', sensor_data),
]

router = DefaultRouter()
router.register(r'session', SessionViewSet)

app_urls = urls + router.urls
