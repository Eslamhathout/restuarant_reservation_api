from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from model_mommy import mommy
from datetime import date
from reservation.models import Reservation, Table
from reservation.serializers import (AvailableSerializer, ReservationCheckSerializer,
                          ReservationDetailSerializer, ReservationsSerializer,
                          TableDetailSerializer)

RESERVATION_URL = reverse('reservation:reservation-list')
TABLE_URL = reverse('reservation:table-list')

class ReservationApiTests(TestCase):
    """Tests for reservation APIs"""

    def setUp(self):
        self.client = APIClient()
        self.employee_user = get_user_model().objects.create_user(
            email='ih@gmail.com',
            password=232323,
            id_number=3636,
            role='Employee'
        )
        self.admin = get_user_model().objects.create_user(
            email='eslam@gmail.com',
            password='password',
            id_number=7836,
            role='Admin'
        )
        self.table_obj = mommy.make(Table)
        self.reservation_obj = mommy.make(Reservation, date=date.today(), table=self.table_obj)
    
    def tearDown(self):
        Table.objects.all().delete()
        Reservation.objects.all().delete()
    

    def test_login_required_for_reservation_listing(self):
        """Test that login is not required for table list"""
        res = self.client.get(RESERVATION_URL)
        self.assertNotEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_reservations_list(self):
        """Test retreving reservations listing for logged in user"""

        self.client.force_authenticate(self.admin)
        res = self.client.get('/api/reservation/reservations-list/')

        reservations = Reservation.objects.all()
        serializer = ReservationsSerializer(reservations, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
    
    def test_retrieve_todays_reservations_list(self):
        """Test retreving todays reservations listing for logged in user"""

        self.client.force_authenticate(self.admin)
        res = self.client.get('/api/reservation/todays-reservations/')

        reservations = Reservation.objects.filter(date=date.today())
        serializer = ReservationsSerializer(reservations, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)




class TableApisTests(TestCase):
    """Tests for table related APIs"""

    def setUp(self):
        self.client = APIClient()
        self.employee_user = get_user_model().objects.create_user(
            email='ih@gmail.com',
            password=232323,
            id_number=3636,
            role='Employee'
        )
        self.admin = get_user_model().objects.create_user(
            email='eslam@gmail.com',
            password='password',
            id_number=7836,
            role='Admin'
        )
        self.table_obj = mommy.make(Table)
        self.reservation_obj = mommy.make(Reservation, date=date.today(), table=self.table_obj)
    
    def tearDown(self):
        Table.objects.all().delete()
        Reservation.objects.all().delete()


    def test_login_required_for_table_listing(self):
        """Test that login is not required for table list"""
        res = self.client.get(TABLE_URL)
        self.assertNotEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_table_list(self):
        """Test retreving table listing for logged in user"""

        self.client.force_authenticate(self.admin)
        res = self.client.get(TABLE_URL)

        tables = Table.objects.all().order_by('table_number')
        serializer = TableDetailSerializer(tables, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_table_employee(self):
        """Test create table restricted for employees"""

        self.client.force_authenticate(self.employee_user)
        res = self.client.post(TABLE_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_table_admin_with_same_number_faliure(self):
        """Test create table for admin users with same table_number"""
        data = {
            "table_number": self.table_obj.table_number,
            "table_capacity": 4
        }
        self.client.force_authenticate(self.admin)
        res = self.client.post('/api/reservation/tables/', data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_table_admin_success(self):
        """Test create table for admin users"""
        data = {
            "table_number": 6,
            "table_capacity": 4
        }
        self.client.force_authenticate(self.admin)
        res = self.client.post('/api/reservation/tables/', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


