from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from model_mommy import mommy

from reservation.models import Reservation, Table
from reservation.serializers import (AvailableSerializer, ReservationCheckSerializer,
                          ReservationDetailSerializer, ReservationsSerializer,
                          TableDetailSerializer)

RESERVATION_URL = reverse('reservation:reservation-list')
TABLE_URL = reverse('reservation:table-list')

class ReservationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_login_required_for_dog_listing(self):
        """Test that login is not required for dogs list"""
        res = self.client.get(TABLE_URL)
        self.assertNotEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_retrieve_dogs_list(self):
    #     """Test retreving dog listing"""
    #     pet_obj = mommy.make(Pet)
    #     breed_obj = mommy.make(Breed)
    #     dog_obj = mommy.make(Dog, breed=breed_obj, pet=pet_obj)

    #     res = self.client.get(DOG_URL)

    #     dogs = Dog.objects.all().order_by('id')
    #     serializer = DogSerializer(dogs, many=True)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
