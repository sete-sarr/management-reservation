from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.UserBookingsListView.as_view(), name='booking_list'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('<str:destination_name>/create/', views.BookingCreateView.as_view(), name='booking_create'),
    path('<int:pk>/cancel/', views.BookingCancelView.as_view(), name='booking_cancel'),
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]
