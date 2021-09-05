from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservation import views

router = DefaultRouter()
# router.register('reservations', views.ReservationsListView)
router.register('reserve', views.ReservationView)
router.register('check', views.ReservationCheckView)
router.register('tables', views.TableView)
# router.register('available', views.AvailableView)

router.register('reservations-list', views.ReservationsListView)
# router.register('todays-reservations', views.TodaysReservationsListView)

app_name = 'reservation'

urlpatterns = [
    path('', include(router.urls)),
    # path('available/<int:number_of_person>', views.available_list),
]