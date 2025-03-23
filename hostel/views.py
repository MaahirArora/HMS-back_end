from django.shortcuts import render
from .models import Room

def home(request):
    rooms = Room.objects.all()
    return render(request, 'hostel/home.html', {'rooms': rooms})
