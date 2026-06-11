from django.urls import path

from .views import (
    booking_cancel,
    booking_create,
    booking_list,
    master_dashboard,
    master_update_status,
)

urlpatterns = [
    path("", booking_list, name="booking_list"),
    path("create/<int:service_id>/", booking_create, name="booking_create"),
    path("<int:pk>/cancel/", booking_cancel, name="booking_cancel"),
    path("master/", master_dashboard, name="master_dashboard"),
    path("master/<int:pk>/update/", master_update_status, name="master_update_status"),
]
