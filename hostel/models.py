from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class StudentManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, phone, password, **extra_fields)


class Student(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    room = models.ForeignKey('Room', on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(default='Student', max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']  # Only include fields required in the form

    objects = StudentManager()  # ✅ Attach custom manager


    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)
    issue = models.TextField(blank=True, null=True)
    
    @property
    def status(self):
        if self.occupied == 0:
            return "Vacant"
        elif self.occupied < self.capacity:
            return "Partially Occupied"
        else:
            return "Occupied"

    def __str__(self):
        return f"Room {self.room_number}"

class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} booked {self.room.room_number}"
    
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    complaint_text = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.student.name} on {self.date_submitted}"
