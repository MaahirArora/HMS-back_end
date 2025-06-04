from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from rest_framework import viewsets, status
from django.http import JsonResponse
from .models import Student, Room, Booking, Complaint
from .serializers import StudentSerializer, RoomSerializer, BookingSerializer, ComplaintSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Registration successful',
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Login successful',
                'tokens': tokens
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


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
        students = Student.objects.select_related('room').all() # optimizing query
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

@csrf_exempt
def new_complaint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_email = data.get('student_email')
            complaint_text = data.get('complaint_text')

            if not student_email or not complaint_text:
                return JsonResponse({'error': 'student_email and complaint_text are required.'}, status=400)

            student = Student.objects.get(email=student_email)
            complaint = Complaint.objects.create(
                student=student,
                complaint_text=complaint_text,
                status='Open',
                date_submitted=timezone.now()
            )

            return JsonResponse({'message': 'Complaint submitted successfully.', 'complaint_id': complaint.id}, status=201)
        
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST method required.'}, status=405)


def list_complaints(request):
    if request.method == 'GET':
        complaints = Complaint.objects.select_related('student').order_by('-date_submitted')
        data = []
        for c in complaints:
            data.append({
                'id': c.id,
                'student_name': c.student.name,
                'student_room': c.student.room.room_number,
                'complaint_text': c.complaint_text,
                'date_submitted': c.date_submitted.isoformat(),
                'status': c.status,
            })
        return JsonResponse(data, safe=False)
    
    return JsonResponse({'error': 'GET method required.'}, status=405)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# class ComplaintViewSet(viewsets.ModelViewSet):
#     queryset = Complaint.objects.all()
#     serializer_class = ComplaintSerializer


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def create(self, request, *args, **kwargs):
        student_email = request.data.get("student_email")
        complaint_text = request.data.get("complaint_text")
        status_ = request.data.get("status", "Open")

        try:
            student = Student.objects.get(email=student_email)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_400_BAD_REQUEST)

        complaint = Complaint.objects.create(
            student=student,
            complaint_text=complaint_text,
            status=status_,
        )
        return Response(ComplaintSerializer(complaint).data, status=status.HTTP_201_CREATED)


def home(request):
    rooms = Room.objects.all()
    return render(request, 'hostel/home.html', {'rooms': rooms})
