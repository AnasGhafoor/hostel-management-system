from django.contrib import admin
from .models import Room, Student, Payment

# --------------------
# Custom Admin for Room
# --------------------
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_no',
        'total_seats',
        'occupied_seats_display',
        'available_seats_display',
        'status'
    )
    search_fields = ('room_no',)
    list_filter = ('status',)
    ordering = ('room_no',)

    def occupied_seats_display(self, obj):
        return obj.occupied_seats()   # 👈 method ko call kiya
    occupied_seats_display.short_description = "Occupied Seats"

    def available_seats_display(self, obj):
        return obj.available_seats()  # 👈 method ko call kiya
    available_seats_display.short_description = "Available Seats"


# ----------------------
# Custom Admin for Student
# ----------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'father_name',
        'cnic',
        'room',
        'admission_date',
        'has_bike',
        'bike_number'
    )
    search_fields = ('name', 'cnic', 'father_name', 'contact')
    list_filter = ('has_bike', 'room', 'admission_date')
    ordering = ('name',)


# ----------------------
# Custom Admin for Payment
# ----------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'month',
        'rent_amount',
        'mess_bill',
        'extra',
        'total',
        'status'
    )
    list_filter = ('status', 'month')
    search_fields = ('student__name', 'student__cnic', 'month')
    ordering = ('-month',)
