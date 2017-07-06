from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views.session import SessionViewSet
from .views.login import login
from .views.sensordata import sensor_data
from .views.touchevents import touch_event
from .views.apns import apns_register
from .views.pretest_survey import pretest_survey

urls = [
    # Login
    url(r'^login/$', login),

    # Data
    url(r'^sensordata/$', sensor_data),
    url(r'^touchevent/$', touch_event),

    # APNS
    url(r'^apns/$', apns_register),

    # Surveys
    url(r'^survey/pretest/$', pretest_survey)
]

router = DefaultRouter()
router.register(r'session', SessionViewSet)

app_urls = urls + router.urls
