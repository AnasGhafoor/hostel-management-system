from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import Student, Room, Payment
from .forms import StudentForm, RoomForm, PaymentForm


# ---------------- Authentication Views ----------------
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "hostel/login.html")


@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def home(request):
    return render(request, "hostel/home.html")


# ---------------- Room Views ----------------
@login_required(login_url="login")
def room_list(request):
    rooms = Room.objects.all()
    room_data = []

    for room in rooms:
        students = Student.objects.filter(room=room)
        room_data.append({
            "room": room,
            "total_seats": room.total_seats,
            "occupied": room.occupied_seats(),
            "available": room.available_seats(),
            "students": students,
        })

    return render(request, "hostel/room_list.html", {"room_data": room_data})


@login_required(login_url="login")
def room_add(request):
    form = RoomForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            room_no = form.cleaned_data.get("room_no")
            if Room.objects.filter(room_no=room_no).exists():
                messages.error(request, f"Room {room_no} already exists.")
            else:
                form.save()
                messages.success(request, "Room added successfully.")
                return redirect("room_list")
    return render(request, "hostel/room_form.html", {"form": form, "title": "Add Room"})


@login_required(login_url="login")
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(request.POST or None, instance=room)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully.")
            return redirect("room_list")
    return render(request, "hostel/room_form.html", {"form": form, "title": "Edit Room"})


@login_required(login_url="login")
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        room.delete()
        messages.success(request, "Room deleted successfully.")
        return redirect("room_list")
    return render(request, "hostel/room_confirm_delete.html", {"room": room})


# ---------------- Student Views ----------------
@login_required(login_url="login")
def student_list(request):
    students = Student.objects.select_related("room").all()
    return render(request, "hostel/student_list.html", {"students": students})


@login_required(login_url="login")
def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            room = student.room
            if room and room.available_seats() <= 0:
                messages.error(request, f"Room {room.room_no} is full.")
            else:
                student.save()
                messages.success(request, "Student added successfully.")
                return redirect("student_list")
    else:
        form = StudentForm()

    rooms = Room.objects.filter(status="Available")
    return render(request, "hostel/student_form.html", {
        "form": form,
        "title": "Add Student",
        "rooms": rooms,
    })


@login_required(login_url="login")
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            updated_student = form.save(commit=False)
            room = updated_student.room
            if room and room.available_seats() <= 0 and updated_student.room != student.room:
                messages.error(request, f"Room {room.room_no} is full.")
            else:
                updated_student.save()
                messages.success(request, "Student updated successfully.")
                return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    rooms = Room.objects.filter(status="Available")
    return render(request, "hostel/student_form.html", {
        "form": form,
        "title": "Edit Student",
        "rooms": rooms,
    })


@login_required(login_url="login")
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")
    return render(request, "hostel/student_confirm_delete.html", {"student": student})


# ---------------- Payment Views ----------------
@login_required(login_url="login")
def payment_list(request):
    payments = Payment.objects.select_related("student").all()
    return render(request, "hostel/payment_list.html", {"payments": payments})


@login_required(login_url="login")
def payment_add(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment recorded successfully.")
            return redirect("payment_list")
    else:
        form = PaymentForm()
    return render(request, "hostel/payment_form.html", {"form": form, "title": "Add Payment"})


@login_required(login_url="login")
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment updated successfully.")
            return redirect("payment_list")
    else:
        form = PaymentForm(instance=payment)
    return render(request, "hostel/payment_form.html", {"form": form, "title": "Edit Payment"})


@login_required(login_url="login")
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        payment.delete()
        messages.success(request, "Payment deleted successfully.")
        return redirect("payment_list")
    return render(request, "hostel/payment_confirm_delete.html", {"payment": payment})


# ---------------- Signup View ----------------
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can login now.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "hostel/signup.html", {"form": form})
