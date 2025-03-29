from django.db import models

class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.roll_number} - {self.name}"

class Room(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied'),
        ('partial', 'Partially Occupied')
    ]
    
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='vacant')
    occupants = models.ManyToManyField(Student, blank=True, related_name="rooms")
    
    def __str__(self):
        return f"Room {self.room_number} ({self.get_status_display()})"

class Event(models.Model):
    name = models.CharField(max_length=200)
    timeline = models.DateTimeField()
    description = models.TextField()
    
    def __str__(self):
        return self.name
