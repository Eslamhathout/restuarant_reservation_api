
from rest_framework import serializers
from reservation.models import Reservation, Table


class ReservationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_field = ('id',)


class ReservationCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('number_of_person', 'date')
        read_only_field = ('id',)


class TableDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'
        read_only_field = ('id',)


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('date', 'start_time', 'end_time', 'table')


class AvailableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('number_of_person', )
