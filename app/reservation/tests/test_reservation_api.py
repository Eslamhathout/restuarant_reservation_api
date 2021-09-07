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
from utils import constants

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


    def test_create_a_reservation_success(self):
        """Test create a reservation by admin user"""

        self.client.force_authenticate(self.admin)

        data = {
            "number_of_person": 4,
            "reservation_name": "er",
            "start_time": "17:00",
            "end_time": "18:00",
            "date": "2021-09-07",
            "table": self.table_obj.table_number
        }

        res = self.client.post('/api/reservation/reserve/', data)
        created_Reservation = Reservation.objects.filter(table=self.table_obj)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_two_reservations_same_time_invalid(self):
        """Test create two reservations in the same time by admin user"""

        self.client.force_authenticate(self.admin)

        data = {
            "number_of_person": 4,
            "reservation_name": "er",
            "start_time": "17:00",
            "end_time": "18:00",
            "date": "2021-09-07",
            "table": self.table_obj.table_number
        }

        res = self.client.post('/api/reservation/reserve/', data)
        res_2 = self.client.post('/api/reservation/reserve/', data)
        created_Reservation = Reservation.objects.filter(table=self.table_obj)
        self.assertEqual(len(created_Reservation), 1)
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.data['message'], constants.TABLE_CAPACITY_ERROR)


    def test_create_a_reservation_in_the_past_invalid(self):
        """Test create a reservation by admin user in the past invalid"""

        self.client.force_authenticate(self.admin)

        data = {
            "number_of_person": 4,
            "reservation_name": "er",
            "start_time": "17:00",
            "end_time": "18:00",
            "date": "2021-09-01",
            "table": self.table_obj.table_number
        }

        res = self.client.post('/api/reservation/reserve/', data)
        created_Reservation = Reservation.objects.filter(table=self.table_obj)
        self.assertEqual(len(created_Reservation), 1)
        self.assertEqual(res.data['message'], constants.RESERVATION_DATE_IN_THE_PAST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_check_reservation_in_the_past_invalid(self):
        """Test create a reservation by admin user in the past invalid"""

        self.client.force_authenticate(self.admin)

        data = {
            "number_of_person": 4,
            "date": "2021-04-01",
        }

        res = self.client.post('/api/reservation/check/', data)
        self.assertEqual(res.data['message'], constants.RESERVATION_DATE_IN_THE_PAST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_a_reservation_for_more_than_12(self):
        """Test create a reservation by admin user for more than 12 invalid"""

        self.client.force_authenticate(self.admin)

        data = {
            "number_of_person": 14,
            "reservation_name": "er",
            "start_time": "17:00",
            "end_time": "18:00",
            "date": "2021-09-08",
            "table": self.table_obj.table_number
        }

        res = self.client.post('/api/reservation/reserve/', data)
        created_Reservation = Reservation.objects.filter(table=self.table_obj)
        self.assertEqual(len(created_Reservation), 1)
        self.assertEqual(res.data['message'], constants.RESERVATION_FOR_MORE_THAN_12_OR_LESS_THAN_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_a_reservation_for_less_than_1(self):
        """Test create a reservation by admin user for less than 1 person invalid"""

        self.client.force_authenticate(self.admin)

        data = {
            "number_of_person": -1,
            "reservation_name": "er",
            "start_time": "17:00",
            "end_time": "18:00",
            "date": "2021-09-08",
            "table": self.table_obj.table_number
        }

        res = self.client.post('/api/reservation/reserve/', data)
        created_Reservation = Reservation.objects.filter(table=self.table_obj)
        self.assertEqual(len(created_Reservation), 1)
        self.assertEqual(res.data['message'], constants.RESERVATION_FOR_MORE_THAN_12_OR_LESS_THAN_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_reservation_check_success(self):
        """Test check a reservation by admin user"""

        self.client.force_authenticate(self.admin)

        data = {
            "number_of_person": 10,
            "date": "2021-09-08",
        }

        res = self.client.post('/api/reservation/check/', data)
        self.assertEqual(res.data['message'], constants.RESERVATION_CHECK)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


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

    def test_retrieve_table_list_employee_invalid(self):
        """Test retreving table listing for logged in user"""

        self.client.force_authenticate(self.employee_user)
        res = self.client.get(TABLE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_table_employee_invalid(self):
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


    def test_delete_a_table_with_pending_reservations_invalid(self):
        """Test delete table for admin users with pending reservations"""

        self.client.force_authenticate(self.admin)
        res = self.client.delete(f'/api/reservation/tables/{self.table_obj.table_number}/')
        self.assertEqual(res.data['message'], constants.TABLE_DELETE_WITH_PENDING_RESERVATIONS)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_a_table_success(self):
        """Test delete table for admin users"""

        table_obj = mommy.make(Table)
        self.client.force_authenticate(self.admin)
        res = self.client.delete(f'/api/reservation/tables/{table_obj.table_number}/')

        self.assertEqual(res.data['message'], constants.TABLE_DELETE_SUCCESS)


    def test_delete_a_table_employee_invalid(self):
        """Test delete table restricted for empoyee users"""
        data = {
            "table_number": 6,
            "table_capacity": 4
        }
        self.client.force_authenticate(self.employee_user)
        numb_of_tables_before_delete = Table.objects.count()
        res = self.client.delete(f'/api/reservation/tables/{self.table_obj.table_number}/')
        numb_of_tables_after_delete = Table.objects.count()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(numb_of_tables_before_delete, numb_of_tables_after_delete)
