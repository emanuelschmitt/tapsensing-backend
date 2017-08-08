from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views.statistics import statistics
from .views.session import SessionViewSet
from .views.login import login
from .views.sensordata import sensor_data
from .views.touchevents import touch_event
from .views.apns import apns_register
from .views.pretest_survey import pretest_survey
from .views.final_survey import final_survey
from .views.trial_settings import trial_settings

urls = [
    # Login
    url(r'^login/$', login),

    # Data
    url(r'^sensordata/$', sensor_data),
    url(r'^touchevent/$', touch_event),

    # APNS
    url(r'^apns/$', apns_register),

    # Surveys
    url(r'^survey/pretest/$', pretest_survey),
    url(r'^survey/final/$', pretest_survey),

    # Statistics
    url(r'^statistics/$', statistics),

    # Settings
    url(r'^trial-settings/$', trial_settings)
]

router = DefaultRouter()
router.register(r'session', SessionViewSet)

app_urls = urls + router.urls
