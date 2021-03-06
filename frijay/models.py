'''Models for the frijay app are created here.

Models created:
Event: a dinner event that is hosted/joined by people
Reservation: a reservation for a dinner event, only accessible to
authenticated users
'''
from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """A model for event attended by users"""
    title = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    # Street Address, Line 1, required
    address = models.CharField("Street Address", max_length=40)
    address2 = models.CharField("Apt / Floor", max_length=40, null=True)
    city = models.CharField("City", max_length=200)
    state = models.CharField("State", max_length=20)
    zipcode = models.CharField("ZIP code", max_length=5)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.BigIntegerField("Phone")
    date = models.DateField("Date")
    time1 = models.TimeField("Starting at")
    time2 = models.TimeField("Ending at")
    openSeats = models.IntegerField("Available Seats")
    additionalDetails = models.TextField("Details",
                                         blank=True,
                                         null=True)

    def __str__(self):
        """Makes the string representation equal to the title of the Event"""
        return self.title


class Reservation(models.Model):
    """Model for a reservation to a dinner"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    accept = models.NullBooleanField(null=True, default=None)

    def __str__(self):
        """Makes the string representation equal to the title of the
        event for which the reservation is being made.
        """
        return self.event.name
