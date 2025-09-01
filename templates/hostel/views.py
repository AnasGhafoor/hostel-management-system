from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from .forms import RoomForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Student

def room_list(request):
    rooms = Room.objects.all()
    room_data = []

    for room in rooms:
        total_seats = room.total_seats
        students_in_room = Student.objects.filter(room=room)
        occupied_seats = students_in_room.count()
        available_seats = total_seats - occupied_seats

        room_data.append({
            'room': room,
            'total_seats': total_seats,
            'occupied': occupied_seats,  # HTML key ke hisaab se match
            'available_seats': available_seats,
            'students': students_in_room
        })

    context = {'room_data': room_data}
    return render(request, 'hostel/room_list.html', context)

# Edit Room
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'hostel/room_form.html', {'form': form, 'title': 'Edit Room'})

# Delete Room
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'hostel/room_delete.html', {'room': room})
