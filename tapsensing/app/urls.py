from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views.login import login
from .views.session import SessionViewSet

urls = [
    # Login
    url(r'^login/$', login)
]

router = DefaultRouter()
router.register(r'session', SessionViewSet)

app_urls = urls + router.urls
