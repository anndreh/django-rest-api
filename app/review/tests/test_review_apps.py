from django.apps import apps
from django.test import TestCase
from review.apps import ReviewConfig


class ReviewConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ReviewConfig.name, 'review')
        self.assertEqual(apps.get_app_config('review').name, 'review')
