from django.contrib import admin
from reservation import models


admin.site.register(models.Reservation)
admin.site.register(models.Table)
