from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@email.com',
            password='123456'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='123456',
            name='Full Name'
        )


    def test_users_listed(self):
        """Test users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        resp = self.client.get(url)

        self.assertContains(resp, self.user.name)
        self.assertContains(resp, self.user.email)

    def test_user_chagen_page(self):
        """Test the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse('admin:core_user_add')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
