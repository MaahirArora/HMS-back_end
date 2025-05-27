from django.urls import path, include
from djangorestframework import routers
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, RoomViewSet, BookingViewSet, ComplaintViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'complaints', ComplaintViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
