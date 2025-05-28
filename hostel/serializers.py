# hostel/serializers.py

from rest_framework import serializers
from .models import Student, Room, Booking, Complaint

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'phone', 'room']

class RoomSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = '__all__'  # This will include all fields in the Room model

    def get_status(self, obj):
        return obj.status  # This calls your @property status method

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'start_date', 'end_date']

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['id', 'complaint_text', 'status', 'date_submitted']
