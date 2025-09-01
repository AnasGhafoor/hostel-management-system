from django import forms
from .models import Room, Student, Payment

# Room form
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_no', 'type', 'status', 'rent']
        widgets = {
            'room_no': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=[('Empty','Empty'),('Occupied','Occupied')]),
            'rent': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Student form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'gender', 'room', 'has_bike', 'bike_number']   # 👈 new fields added
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[('Male','Male'),('Female','Female')]),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'has_bike': forms.CheckboxInput(attrs={'class': 'form-check-input'}),   # 👈 new widget
            'bike_number': forms.TextInput(attrs={'class': 'form-control'}),        # 👈 new widget
        }

# Payment form
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'amount', 'date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
