from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Review
from review.serializers import ReviewSerializer


REVIEW_URL = reverse('review:review-list')


def detail_url(review_id):
    """Return review detail URL"""
    return reverse('review:review-detail', args=[review_id])


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
        self.user2 = get_user_model().objects.create_user(
            'test2@email.com',
            '654321'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_reviews(self):
        """Test retrieving a list of reviews"""
        sample_review(user=self.user)
        sample_review(user=self.user)

        resp = self.client.get(REVIEW_URL)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_review_limited_to_user(self):
        """Teste retrieving reviews for user"""
        sample_review(user=self.user)
        sample_review(user=self.user2)

        resp = self.client.get(REVIEW_URL)

        reviews = Review.objects.filter(user=self.user)
        serializer = ReviewSerializer(reviews, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data, serializer.data)

    def test_create_review(self):
        """Test creating review"""
        payload = {
            'title': 'Not Bad!',
            'ip_address': '127.0.0.2',
            'rating': 3,
            'summary': 'I am disapointed',
            'submission_date': '2019-05-03',
            'company': 'Unhappy Stores',
        }
        resp = self.client.post(REVIEW_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        review = Review.objects.get(id=resp.data['id'])
        for key in payload.keys():
            if key == 'submission_date':
                payload[key] = datetime.strptime(
                    payload[key], '%Y-%m-%d').date()
            self.assertEqual(payload[key], getattr(review, key))

    def test_partial_update_review(self):
        """Test updating a review with patch"""
        review = sample_review(user=self.user)
        payload = {'title': 'Very Cool Place!'}
        url = detail_url(review.id)

        self.client.patch(url, payload)

        review.refresh_from_db()
        self.assertEqual(review.title, payload['title'])

    def test_full_update_review(self):
        """Test updating a review with put"""
        review = sample_review(user=self.user)
        payload = {
            'title': 'I Completly Dislike It',
            'ip_address': '127.0.0.1',
            'rating': 1,
            'summary': 'Trash Place',
            'submission_date': '2019-05-03',
            'company': 'Somewhere',
        }
        url = detail_url(review.id)
        self.client.put(url, payload)

        review.refresh_from_db()
        self.assertEqual(review.title, payload['title'])
        self.assertEqual(review.ip_address, payload['ip_address'])
        self.assertEqual(review.rating, payload['rating'])
        self.assertEqual(review.summary, payload['summary'])
        self.assertEqual(review.submission_date, datetime.strptime(
                         payload['submission_date'], '%Y-%m-%d').date())
        self.assertEqual(review.company, payload['company'])
