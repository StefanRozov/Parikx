from django.contrib import admin
from .models import Booking, BookingStatus

admin.site.register(Booking)
admin.site.register(BookingStatus)