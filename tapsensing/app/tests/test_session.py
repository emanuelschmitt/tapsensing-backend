import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

from ..models import Session, UserSettings
from ..views.session import SessionViewSet

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
            typing_modality=Session.INDEX_FINGER,
        )

        response = view(request)
        self.assertEquals(response.data["exists"], True)

        session.delete()

        response = view(request)
        self.assertEquals(response.data["exists"], False)

    def testSessionExistsForTodayLabMode(self):
        self.user.usersettings.lab_mode = True

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
        self.assertEquals(response.data["exists"], False)

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

        self.user.usersettings.lab_mode = True
        self.assertEquals(response.data["exists"], False)

    def testSessionExistsTodayWhenCreatedYesterdayLabMode(self):
        self.user.usersettings.lab_mode = True

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

        self.user.usersettings.lab_mode = True
        self.assertEquals(response.data["exists"], False)

    def testNotCompleted(self):
        self.user.usersettings.lab_mode = False

        request = self.factory.get("api/v1/session/exists/")
        force_authenticate(request, user=self.user)
        view = SessionViewSet.as_view({'get': 'exists'})
        response = view(request)

        self.assertEquals(response.data["completed"], False)

        for i in range(4):
            _ = self.createSession()

        view = SessionViewSet.as_view({'get': 'exists'})
        response = view(request)
        self.assertEquals(response.data["completed"], True)

        for i in range(7):
            _ = self.createSession()

        view = SessionViewSet.as_view({'get': 'exists'})
        response = view(request)
        self.assertEquals(response.data["completed"], True)
