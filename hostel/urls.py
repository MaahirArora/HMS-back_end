from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, RoomViewSet, BookingViewSet, ComplaintViewSet, LoginView, RegisterView,BillingViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'complaints', ComplaintViewSet)
router.register(r'billings', BillingViewSet)
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('', include(router.urls)),
]
