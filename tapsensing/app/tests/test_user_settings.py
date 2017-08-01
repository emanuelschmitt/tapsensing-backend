from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Session, UserSettings

USERNAME = 'testuser'
PASSWORD = '123'


class UserSettingsTest(TestCase):
    user = None
    user_settings = None

    def setUp(self):
        self.user = User.objects.create_user(USERNAME, None, PASSWORD)
        self.user_settings = UserSettings.objects.get(user=self.user)

    def tearDown(self):
        User.objects.all().delete()

    def testUserSettingsCreation(self):
        # Test if user settings where created
        self.assertIsInstance(self.user_settings, UserSettings)
        self.assertEqual(self.user_settings.user.pk, self.user.pk, "user settings should be set to user")
        self.assertEqual(self.user_settings.lab_mode, False, "user settings lab mode should default to false")

    def testUserSettingsDeletion(self):
        self.user.delete()
        user_settings = UserSettings.objects.filter(pk=self.user_settings.pk).count()
        self.assertEqual(user_settings, 0, "User settings should be deleted once the user is deleted.")
