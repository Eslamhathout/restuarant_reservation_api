from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import mixins, status
import datetime
from .serializers import ReservationDetailSerializer, TableDetailSerializer, ReservationsSerializer, AvailableSerializer, ReservationCheckSerializer
from .models import Reservation, Table
from utils import constants, helpers
from rest_framework.permissions import (
    IsAuthenticated,
)
from reservation.permissions import IsAdmin
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
import json

from datetime import timedelta, date, time
import datetime

class ReservationView(viewsets.GenericViewSet, generics.CreateAPIView):
    serializer_class = ReservationDetailSerializer
    queryset = Reservation.objects.all()
    permission_classes = (IsAuthenticated,)

    def _get_table_availability(self, table, date_table_availability):
        for table_availability in date_table_availability:
            if int(table_availability['table_number']) == int(table):
                return table_availability['table_availability']
    
    def _check_in_time_range(self, available_range, start_time, end_time):
        """Checks if a given (start and end )time locates in any of the availability ranges"""
        available_range_start, available_range_end = available_range.replace(' ', '').split('-')
        available_range_start_dt = datetime.time(int(available_range_start.split(":")[0]), int(available_range_start.split(":")[1]), 0)
        available_range_end_dt = datetime.time(int(available_range_end.split(":")[0]), int(available_range_end.split(":")[1]), 0)

        start_time_dt = datetime.time(int(start_time.split(":")[0]), int(start_time.split(":")[1]), 0)
        end_time_dt = datetime.time(int(end_time.split(":")[0]), int(end_time.split(":")[1]), 0)

        print(available_range_start_dt, available_range_end_dt)
        print(start_time_dt, end_time_dt)

        return (available_range_start_dt <= start_time_dt <= available_range_end_dt) and (available_range_start_dt <= end_time_dt <= available_range_end_dt)

    def create(self, request, *args, **kwargs):
        reservation_check = ReservationCheckView()
        response_obj = reservation_check.create(request, *args, **kwargs)
        response_obj_data = response_obj.data['data']
        date_table_availability = response_obj.data['data'][request.data['date']]
        print("OOOOOOOOOOOOOO", date_table_availability)

        table_available_start_end = self._get_table_availability(request.data['table'], date_table_availability)
        if not table_available_start_end:
            return Response({'message': "Please make sure you choose a table with capacity more than or equal your required number."})

        reservation_start_time = request.data['start_time']
        reservation_end_time = request.data['end_time']

        print("table_available_start_end: ", table_available_start_end)
        print("reservation_start_time: ", reservation_start_time)
        print("reservation_end_time: ", reservation_end_time)

        for time_range in table_available_start_end:
            if self._check_in_time_range(time_range, reservation_start_time, reservation_end_time):
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        #return availability to choose from
        return Response(f"Sorry there is no availability for the required time-slot. \nhere is the available based on your needs: {response_obj_data}", status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        serializer.save()





class TableView(viewsets.ModelViewSet):
    serializer_class = TableDetailSerializer
    queryset = Table.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin)

    def destroy(self, request, *args, **kwargs):
        table_obj = self.get_object()
        if Reservation.objects.filter(table=table_obj).exists():
            return Response({'message': 'Table can not be deleted as it has pending reservations.'}, status=status.HTTP_400_BAD_REQUEST)
        table_obj.delete()
        return Response({'message': 'Table deleted successfully.'})

class ReservationsListView(viewsets.GenericViewSet, generics.ListAPIView, mixins.ListModelMixin):
    serializer_class = ReservationsSerializer
    queryset = Reservation.objects.all()

# class TodaysReservationsListView(viewsets.GenericViewSet, generics.ListAPIView, mixins.ListModelMixin):
#     serializer_class = ReservationsSerializer
#     queryset = Reservation.objects.filter(date=datetime.datetime.now().date())


class TableView(viewsets.ModelViewSet):
    """Table managment functionality DONE"""

    serializer_class = TableDetailSerializer
    queryset = Table.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin)

    def destroy(self, request, *args, **kwargs):
        table_obj = self.get_object()
        if Reservation.objects.filter(table=table_obj).exists():
            return Response({'message': 'Table can not be deleted as it has pending reservations.'}, status=status.HTTP_400_BAD_REQUEST)
        table_obj.delete()
        return Response({'message': 'Table deleted successfully.'})


class ReservationCheckView(viewsets.GenericViewSet, generics.CreateAPIView):
    serializer_class = ReservationCheckSerializer
    queryset = Reservation.objects.all()
    permission_classes = (IsAuthenticated,)

    def _is_valid_number_of_persons(self, number_of_person):
        """Validates number of persons"""
        return (number_of_person > 12) or (number_of_person < 0)

    def _is_valid_date(self, date_obj):
        """Validates that date not in the past or not in the next 3 days"""
        days = date_obj - date.today()
        if days.days >= 0 and days.days <=3:
            return True
        return False

    def _get_available_slots(self, hours, appointments, duration=timedelta(minutes=15)):
        """ Gets the available solt possible given the fact that the minimum duration shloud be 15 min"""
        if hours[0].date() == date.today():
            hours = (datetime.datetime.combine(date.today(), datetime.datetime.now().time()), hours[1])
        available_slots = [] 
        slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
        # print(max(appointments))
        # print("slots: ", slots)
        # available_slots.append(slots[1])
        if appointments == []:
            print("YYYYYYYYYYYYYYY")
            if hours[0].date() == date.today():
                available_for_rest_of_the_day = datetime.datetime.combine(date.today(), datetime.datetime.now().time())
                return ["{:%H:%M} - {:%H:%M}".format(available_for_rest_of_the_day, hours[1])]
            return hours
        for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
            print("start - end: ", start.time())
            # if start.time() < datetime.now()
            if start + duration <= end:
                diff = end - start
                # available_slots.append((start, start + diff))
                available_slots.append("{:%H:%M} - {:%H:%M}".format(start, start + diff))
        return available_slots

    def _get_table_reservations_for_specific_date(self, day, table_number):
        """ Gets a table reservations for a specific day"""
        now = datetime.datetime.now().time()
        appointments  = []

        day_opening_hours = (datetime.datetime.combine(day, constants.RESTAURANT_OPEN_TIME), datetime.datetime.combine(day, constants.RESTAURANT_CLOSE_TIME))
        table_reservations = Reservation.objects.all().filter(table__table_number=table_number, date=day, start_time__gte=now)
        for reservation in table_reservations:
            appointments.append((datetime.datetime.combine(day, reservation.start_time), datetime.datetime.combine(day, reservation.end_time)))
        print("appointments :", appointments)
        return self._get_available_slots(hours=day_opening_hours, appointments=appointments) 

    def create(self, request, *args, **kwargs):
        number_of_person = int(request.data['number_of_person'])
        target_date = datetime.datetime.strptime(request.data['date'], "%Y-%m-%d").date()

        result_json = {}
        result_json[request.data['date']] = []

        if self._is_valid_number_of_persons(number_of_person):
            return Response("Table capacity should be between 1: 12")

        if not self._is_valid_date(target_date):
            return Response("Date can't be in the past or far from 3 days.")

        available_tables_with_capacity_gte_requested_qs = Table.objects.filter(table_capacity__gte=int(number_of_person)).order_by('table_capacity')

        for best_fit_table in available_tables_with_capacity_gte_requested_qs:
            available_time_slots_for_a_table_in_a_day = self._get_table_reservations_for_specific_date(target_date, best_fit_table.table_number)
            result_json[request.data['date']].append({'table_number': best_fit_table.table_number, 'table_capacity': best_fit_table.table_capacity, 'table_availability': available_time_slots_for_a_table_in_a_day})
        print(json.dumps(result_json, indent=14, sort_keys=True))
        return Response({'message': 'Available slot for the tables that fits the required number of people sorted by bestFit first.', 'data': result_json})
