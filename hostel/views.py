from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def room_list_api(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        data = []

        for room in rooms:
            # Optional: assume `issue` exists in Room model
            # issue = getattr(room, 'issue', None)
            
            # Determine room status
            # if issue:
            #     status = "Maintenance"
            if room.occupied == room.capacity:
                status = "Occupied"
            elif room.occupied > 0:
                status = "Partially Occupied"
            else:
                status = "Vacant"

            data.append({
                'id': room.id,
                'room_number': room.room_number,
                'capacity': room.capacity,
                'occupied': room.occupied,
                'status': status,
            })

        return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'GET method required'}, status=405)


@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            room_id = data.get('room')  # expects room ID

            if not all([name, email, phone, room_id]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            try:
                room = Room.objects.get(id=room_id)
            except Room.DoesNotExist:
                return JsonResponse({'error': 'Room not found.'}, status=404)

            if room.occupied >= room.capacity:
                return JsonResponse({'error': 'Room is already full.'}, status=400)

            # Create student and assign room
            student = Student.objects.create(
                name=name,
                email=email,
                phone=phone,
                room=room
            )

            # Increment room occupancy
            room.occupied += 1
            room.save()

            return JsonResponse({'message': 'Student added successfully.', 'id': student.id})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


def home(request):
    rooms = Room.objects.all()
    return render(request, 'hostel/home.html', {'rooms': rooms})
