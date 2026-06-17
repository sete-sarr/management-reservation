from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from datetime import date
from .models import Booking
from destinations.models import Destination
from payments.models import Payment


class BookingCreateView(LoginRequiredMixin, CreateView):
    """View to create a new booking."""
    model = Booking
    template_name = 'bookings/booking_form.html'
    fields = ['travel_start_date', 'travel_end_date', 'number_of_people', 'special_requests']
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = get_object_or_404(Destination, name=self.kwargs.get('destination_name'))
        context['destination'] = destination
        context['available_slots'] = destination.get_available_remaining()
        return context
    
    def form_valid(self, form):
        destination = get_object_or_404(Destination, name=self.kwargs.get('destination_name'))
        
        # Validate dates
        if form.cleaned_data['travel_start_date'] <= date.today():
            messages.error(self.request, 'Travel date must be in the future.')
            return self.form_invalid(form)
        
        if form.cleaned_data['travel_end_date'] <= form.cleaned_data['travel_start_date']:
            messages.error(self.request, 'End date must be after start date.')
            return self.form_invalid(form)
        
        # Check availability
        available_slots = destination.get_available_remaining()
        if form.cleaned_data['number_of_people'] > available_slots:
            messages.error(self.request, f'Only {available_slots} slots available.')
            return self.form_invalid(form)
        
        booking = form.save(commit=False)
        booking.user = self.request.user
        booking.destination = destination
        booking.total_price = destination.price_per_person * form.cleaned_data['number_of_people']
        booking.save()
        
        messages.success(self.request, f'Booking created! Confirmation code: {booking.confirmation_code}')
        return redirect('bookings:booking_detail', pk=booking.pk)


class UserBookingsListView(LoginRequiredMixin, ListView):
    """View to display user's bookings."""
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10
    login_url = 'users:login'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_spent'] = sum(b.total_price for b in self.get_queryset())
        context['confirmed_bookings'] = self.get_queryset().filter(status='confirmed').count()
        context['pending_bookings'] = self.get_queryset().filter(status='pending').count()
        return context


class BookingDetailView(LoginRequiredMixin, DetailView):
    """View to display booking details."""
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'
    login_url = 'users:login'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = self.get_object()
        
        try:
            context['payment'] = Payment.objects.get(booking=booking)
        except Payment.DoesNotExist:
            context['payment'] = None
        
        context['days_until_travel'] = (booking.travel_start_date - date.today()).days
        context['can_cancel'] = booking.can_be_cancelled()
        
        return context


class BookingCancelView(LoginRequiredMixin, View):
    """View to cancel a booking."""
    login_url = 'users:login'

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        
        if not booking.can_be_cancelled():
            messages.error(request, 'This booking cannot be cancelled.')
            return redirect('bookings:booking_detail', pk=pk)
        
        booking.status = 'cancelled'
        booking.save()
        
        messages.success(request, f'Booking {booking.confirmation_code} has been cancelled.')
        return redirect('bookings:booking_list')


class AdminDashboardView(LoginRequiredMixin, View):
    """Admin dashboard view."""
    login_url = 'users:login'

    def get(self, request):
        # Check if user is admin
        if not (request.user.is_superuser or request.user.profile.role == 'admin'):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('destinations:home')
        
        context = {
            'total_bookings': Booking.objects.count(),
            'confirmed_bookings': Booking.objects.filter(status='confirmed').count(),
            'pending_bookings': Booking.objects.filter(status='pending').count(),
            'cancelled_bookings': Booking.objects.filter(status='cancelled').count(),
            'total_revenue': sum(b.total_price for b in Booking.objects.filter(status='confirmed')),
            'total_destinations': Destination.objects.count(),
            'total_users': Booking.objects.values('user').distinct().count(),
            'recent_bookings': Booking.objects.order_by('-created_at')[:10],
        }
        
        return render(request, 'admin/dashboard.html', context)
