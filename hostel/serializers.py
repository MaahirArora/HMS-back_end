# hostel/serializers.py
from rest_framework import serializers
from .models import Student, Room, Booking, Complaint
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class StudentRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # ✅ Add this line to avoid the missing username error
        validated_data['username'] = validated_data['email']

        user = Student.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # This will include all fields in the Student model

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
