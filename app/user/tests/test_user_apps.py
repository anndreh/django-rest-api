from django.apps import apps
from django.test import TestCase
from user.apps import UserConfig


class UserConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(UserConfig.name, 'user')
        self.assertEqual(apps.get_app_config('user').name, 'user')
