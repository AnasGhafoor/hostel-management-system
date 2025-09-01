from django.db import models

# hostel/models.py

class Room(models.Model):
    room_no = models.CharField(max_length=10, unique=True)
    total_seats = models.PositiveIntegerField()
    rent = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Available', 'Available'),
            ('Full', 'Full'),
            ('Maintenance', 'Maintenance')
        ],
        default='Available'
    )

    def occupied_seats(self):
        return self.students.count()   # ✅ updated

    def available_seats(self):
        return self.total_seats - self.occupied_seats()

    def __str__(self):
        return f"Room {self.room_no}"



class Student(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=15, unique=True)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    admission_date = models.DateField()
    has_bike = models.BooleanField(default=False)
    bike_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    rent_amount = models.DecimalField(max_digits=8, decimal_places=2)
    mess_bill = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    extra = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unpaid')

    def __str__(self):
        return f"{self.student.name} - {self.month}"
