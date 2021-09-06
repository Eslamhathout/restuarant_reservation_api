from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email"""
        email = 'eslam@rtob.com'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            id_number=3636
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_domain_normalized(self):
        """Test the email for new user is normalized. default is domain is case senstive, so we
        need to change it to case in-sensitive"""

        email = 'eslam@rtOB.COM'
        password = 'testpass'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            id_number=7777
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email faild"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpasswprd')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = 'eslamh@rtOB.COM'
        password = 'testpass'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            id_number=5555
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
