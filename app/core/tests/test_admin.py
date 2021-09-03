from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()

        email = 'eh@PAYMOB.COM'
        email_2 = 'eslamh@PAYMOB.COM'
        password = 'testpass'

        self.admin_user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email=email_2,
            password=password,
            name='Test user full name'
        )
    
    def test_users_listed(self):
        """Test that users are listed"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_create_user_page(self):
        """Test create user"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)



























