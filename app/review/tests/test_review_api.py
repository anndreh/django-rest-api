from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Review
from review.serializers import ReviewSerializer


REVIEW_URL = reverse('review:review-list')


def sample_review(user, **params):
    """Create and return a sample review"""
    defaults = {
        'title': 'Great place to shop!',
        'ip_address': '127.0.0.1',
        'rating': 5,
        'summary': 'I am very happy...',
        'submission_date': '2019-05-01',
        'company': 'Happy Stores',
    }
    defaults.update(params)

    return Review.objects.create(user=user, **defaults)


class PublicReviewApiTests(TestCase):
    """Test unauthenticated review API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        resp = self.client.get(REVIEW_URL)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReviewApiTest(TestCase):
    """Test unauthenticated review API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            '123456'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_reviews(self):
        """Test retrieving a list of reviews"""
        sample_review(user=self.user)
        # sample_review(user=self.user)

        resp = self.client.get(REVIEW_URL)
        reviews = Review.objects.all().order_by('-submission_date')
        # reviews = (Review.objects.filter(user=self.user)
        #            .order_by('-submission_date'))
        serializer = ReviewSerializer

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_review_limited_to_user(self):
        """Teste retrieving reviews for user"""
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            '654321'
        )
        sample_review(user=user2)
        sample_review(user=self.user)

        resp = self.client.get(REVIEW_URL)

        reviews = Review.objects.filter(user=self.user)
        serializer = ReviewSerializer

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data, serializer.data)
