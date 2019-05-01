from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@email.com', password='123456'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email, password)



class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@email.com'
        password = '123456'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123456')

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            '123456'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_review_str(self):
        """Test the review string representaion"""
        review = models.Review.objects.create(
            user=sample_user(),
            title='Great place to shop!',
            ip_address='127.0.0.1',
            rating='5',
            summary='I am very happy...',
            submission_date='2019-05-01',
            company='Happy Stores',
        )

        self.assertEqual(str(review), review.title)

