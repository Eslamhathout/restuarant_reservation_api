from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta


class Table(models.Model):
    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
    
    table_number = models.IntegerField(unique=True, primary_key=True)
    table_capacity = models.IntegerField(default=1,
        validators=[MaxValueValidator(12), MinValueValidator(1)]
     )

    def __str__(self):
        return f'Table: {self.table_number}'

class Reservation(models.Model):
    number_of_person = models.IntegerField()
    reservation_name = models.CharField(max_length=100)
    table = models.ForeignKey('Table', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField(null=True)

    def __str__(self):
        return f'Reservation: {self.reservation_name}'

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        unique_together = ('table', 'start_time', 'date')
