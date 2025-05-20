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

def student_list_api(request):
    if request.method == 'GET':
        students = Student.objects.select_related('room').all()
        data = []

        for student in students:
            data.append({
                'id': student.id,
                'name': student.name,
                'email': student.email,
                'phone': student.phone,
                'room': student.room.room_number if student.room else None,
            })

        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'GET method required'}, status=405)

@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'DELETE':
        try:
            student = Student.objects.get(id=student_id)
            room = student.room
            student.delete()

            if room:
                room.occupied = max(room.occupied - 1, 0)
                room.save()

            return JsonResponse({'message': 'Student deleted successfully'})
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)

@csrf_exempt
def create_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            student_id = data.get('student_id')
            room_id = data.get('room_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not all([student_id, room_id, start_date, end_date]):
                return JsonResponse({'error': 'Missing fields'}, status=400)

            student = Student.objects.get(id=student_id)
            room = Room.objects.get(id=room_id)

            # Check overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_date__lte=end_date,
                end_date__gte=start_date
            ).count()

            if overlapping_bookings >= room.capacity:
                return JsonResponse({'error': 'Room is fully booked for the selected period.'}, status=400)

            # Create booking
            booking = Booking.objects.create(
                student=student,
                room=room,
                start_date=start_date,
                end_date=end_date
            )

            return JsonResponse({'message': 'Booking created', 'id': booking.id})

        except (Student.DoesNotExist, Room.DoesNotExist):
            return JsonResponse({'error': 'Student or Room not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'POST method required'}, status=405)

def booking_list_api(request):
    if request.method == 'GET':
        bookings = Booking.objects.select_related('student', 'room').all()
        data = []

        for booking in bookings:
            data.append({
                'id': booking.id,
                'student': booking.student.name,
                'room': booking.room.room_number,
                'start_date': booking.start_date,
                'end_date': booking.end_date,
            })

        return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'GET method required'}, status=405)


def home(request):
    rooms = Room.objects.all()
    return render(request, 'hostel/home.html', {'rooms': rooms})
