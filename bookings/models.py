from django.db import models
from core.models import User
from services.models import Service

class BookingStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Booking(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='master_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.ForeignKey(BookingStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client.username} — {self.service.name} ({self.date:%d.%m.%Y %H:%M})"