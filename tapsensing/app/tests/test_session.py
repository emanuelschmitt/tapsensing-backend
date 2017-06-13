import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from ..models import Session
from ..views.session import SessionViewSet

USERNAME = 'testuser'
PASSWORD = '123'


class SessionTests(TestCase):
    user = None
    factory = None

    def setUp(self):
        self.user = User.objects.create_user(USERNAME, None, PASSWORD)
        self.factory = APIRequestFactory()

    def tearDown(self):
        User.objects.all().delete()
        Session.objects.all().delete()

    def testSessionExistsForToday(self):
        request = self.factory.get("api/v1/session/exists/")
        force_authenticate(request, user=self.user)

        view = SessionViewSet.as_view({'get': 'exists'})
        response = view(request)

        self.assertEquals(response.data["exists"], False)

        session = Session.objects.create(
            user=self.user,
            date=datetime.datetime.today(),
            body_posture=Session.SITTING,
            typing_modality=Session.INDEX_FINGER
        )

        response = view(request)
        self.assertEquals(response.data["exists"], True)

        session.delete()

        response = view(request)
        self.assertEquals(response.data["exists"], False)

    def testSessionExistsTodayWhenCreatedYesterday(self):
        session = Session.objects.create(
            user=self.user,
            date=datetime.datetime.today() - datetime.timedelta(days=1),
            body_posture=Session.SITTING,
            typing_modality=Session.INDEX_FINGER
        )
        request = self.factory.get("api/v1/session/exists/")
        force_authenticate(request, user=self.user)
        view = SessionViewSet.as_view({'get': 'exists'})
        response = view(request)

        self.assertEquals(response.data["exists"], False)
