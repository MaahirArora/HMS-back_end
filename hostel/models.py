from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)

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
