import datetime

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

from ..models import Session, UserSettings
from ..views.session import SessionViewSet, States

USERNAME = 'testuser'
PASSWORD = '123'


# BEWARE: Heavy 80/20
class SessionTests(TestCase):
    user = None
    factory = None

    def setUp(self):
        self.user = User.objects.create_user(USERNAME, None, PASSWORD)
        self.factory = APIRequestFactory()

    def tearDown(self):
        User.objects.all().delete()
        Session.objects.all().delete()

    def createSession(self, date=datetime.datetime.today(), lab_mode=False):
        return Session.objects.create(
            user=self.user,
            date=date,
            body_posture=Session.SITTING,
            typing_modality=Session.INDEX_FINGER,
            lab_mode=lab_mode
        )

    def testSessionExists(self):
        request = self.factory.get("api/v1/session/exists/")
        force_authenticate(request, user=self.user)

        view = SessionViewSet.as_view({'get': 'exists'})
        response = view(request)

        self.assertEquals(response.data["state"], States.NOT_DONE_TODAY)

        session = self.createSession()

        response = view(request)
        self.assertEquals(response.data["state"], States.DONE_TODAY)

        session.delete()

        response = view(request)
        self.assertEquals(response.data["state"], States.NOT_DONE_TODAY)

    def testSessionLabMode(self):
        self.user.usersettings.lab_mode = True

        request = self.factory.get("api/v1/session/exists/")
        force_authenticate(request, user=self.user)

        view = SessionViewSet.as_view({'get': 'exists'})
        response = view(request)

        self.assertEquals(response.data["state"], States.LAB_MODE)

        session = self.createSession()

        response = view(request)
        self.assertEquals(response.data["state"], States.LAB_MODE)

        session.delete()
        self.user.usersettings.lab_mode = False

        response = view(request)
        self.assertNotEqual(response.data["state"], States.LAB_MODE)

    def testSessionExistsTodayWhenCreatedYesterday(self):
        self.user.usersettings.lab_mode = False

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

        self.assertEquals(response.data["state"], States.NOT_DONE_TODAY)

    def testCompleted(self):
        self.user.usersettings.lab_mode = False

        request = self.factory.get("api/v1/session/exists/")
        force_authenticate(request, user=self.user)
        view = SessionViewSet.as_view({'get': 'exists'})
        response = view(request)

        self.assertEquals(response.data["state"], States.NOT_DONE_TODAY)

        for i in range(settings.AMOUNT_NON_LAB_SESSIONS):
            _ = self.createSession()

        response = view(request)
        self.assertEquals(response.data["state"], States.COMPLETED)

        Session.objects.all().delete()

        response = view(request)
        self.assertNotEqual(response.data["state"], States.DONE_TODAY)
