from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**param): 
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_user_success(self):
        """Test creating user with valid payload"""

        payload = {
            'email': 'ehat@gmail.com',
            'password': 'testp',
            'name': 'TestName',
            'id_number' : 1111,
            'role': 'Employee'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))


    def test_create_valid_admin_user_success(self):
        """Test creating user with valid payload"""

        payload = {
            'email': 'tt@gmail.com',
            'password': 'testp',
            'name': 'TestName',
            'id_number' : 4523,
            'role': 'Admin'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))























