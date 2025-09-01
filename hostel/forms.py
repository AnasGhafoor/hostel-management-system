from django import forms
from django.core.exceptions import ValidationError
from .models import Room, Student, Payment


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_no', 'total_seats', 'rent', 'status']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'father_name', 'cnic', 'contact', 'address',
            'room', 'admission_date', 'has_bike', 'bike_number'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ sirf available rooms dropdown me
        self.fields['room'].queryset = Room.objects.filter(status="Available")
        # ✅ bike_number optional banate hain
        self.fields['bike_number'].required = False

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        has_bike = cleaned_data.get('has_bike')
        bike_number = cleaned_data.get('bike_number')

        # ✅ Room seat validation
        if room and room.available_seats() <= 0:
            raise ValidationError(f"Room {room.room_no} is already full. Please select another room.")

        # ✅ Bike validation
        if has_bike and not bike_number:
            self.add_error('bike_number', "Please enter bike number.")
        if not has_bike:
            cleaned_data['bike_number'] = ''  # agar bike nahi hai to number blank rakho

        return cleaned_data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'student', 'month', 'rent_amount',
            'mess_bill', 'extra', 'total', 'status'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ dropdown me sirf wo students show honge jo already registered hain
        self.fields['student'].queryset = Student.objects.all().order_by('name')
        # ✅ student ka naam ke sath uska room no. bhi show hoga
        self.fields['student'].label_from_instance = (
            lambda obj: f"{obj.name} ({obj.room.room_no if obj.room else 'No Room'})"
        )

