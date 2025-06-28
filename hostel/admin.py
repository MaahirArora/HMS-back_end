from django.contrib import admin
from .models import Student, Room, Booking, Complaint,Billing

admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Complaint)
admin.site.register(Billing)

