from django.db import models
from django.core.exceptions import ValidationError

class Room(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("full", "Full"),
        ("maintenance", "Maintenance"),
    ]

    room_no = models.CharField(max_length=10, unique=True)
    total_seats = models.PositiveIntegerField()
    occupied_seats = models.PositiveIntegerField(default=0)  # ← user se input
    rent = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    def clean(self):
        if self.occupied_seats < 0:
            raise ValidationError({"occupied_seats": "Occupied seats negative nahi ho sakti."})
        if self.occupied_seats > self.total_seats:
            raise ValidationError({"occupied_seats": "Occupied total seats se zyada nahi ho sakti."})

    @property
    def available_seats(self):
        # table mein dikhane ke liye (DB column ki zaroorat nahi)
        return max(self.total_seats - self.occupied_seats, 0)

    def __str__(self):
        return f"Room {self.room_no}"

