from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservation import views

router = DefaultRouter()
router.register('reserve', views.ReservationView)
router.register('check', views.ReservationCheckView)
router.register('tables', views.TableView)
router.register('reservation-destory', views.ReservationsDestoryView)
router.register('reservations-list', views.ReservationsView)
router.register('todays-reservations', views.TodaysReservationsView)

app_name = 'reservation'

urlpatterns = [
    path('', include(router.urls)),
]