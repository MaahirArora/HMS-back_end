from django.contrib import admin
from django.urls import path, include
from hostel import views  # Optional, for home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Assuming you have a home view
    path('api/', include('hostel.urls')),  # DRF endpoints
]
