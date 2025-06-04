# hostel/serializers.py
from rest_framework import serializers
from .models import Student, Room, Booking, Complaint
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['email', 'name', 'phone', 'room', 'password']

    def create(self, validated_data):
        user = Student(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone'],
            room=validated_data.get('room')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}


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

from rest_framework import serializers
from .models import Complaint

class ComplaintSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.name", read_only=True)

    class Meta:
        model = Complaint
        fields = '__all__' 
