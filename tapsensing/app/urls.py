from rest_framework.routers import SimpleRouter
from .views.trail import TrailViewset

router = SimpleRouter()
router.register(r'trail', TrailViewset)

app_urls = router.urls