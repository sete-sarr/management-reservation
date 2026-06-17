from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Review
from destinations.models import Destination
from bookings.models import Booking


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """View to create a review for a destination."""
    model = Review
    template_name = 'reviews/review_form.html'
    fields = ['rating', 'title', 'comment']
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = get_object_or_404(Destination, name=self.kwargs.get('destination_name'))
        context['destination'] = destination
        
        # Check if user has booked this destination
        has_booking = Booking.objects.filter(
            user=self.request.user,
            destination=destination,
            status='confirmed'
        ).exists()
        context['has_booking'] = has_booking
        
        # Check if user already reviewed this destination
        existing_review = Review.objects.filter(
            user=self.request.user,
            destination=destination
        ).first()
        context['existing_review'] = existing_review
        
        return context
    
    def form_valid(self, form):
        destination = get_object_or_404(Destination, name=self.kwargs.get('destination_name'))
        
        # Check if user already reviewed this destination
        existing_review = Review.objects.filter(
            user=self.request.user,
            destination=destination
        )
        
        if existing_review.exists():
            messages.error(self.request, 'You have already reviewed this destination.')
            return redirect('destinations:destination_detail', name=destination.name)
        
        review = form.save(commit=False)
        review.user = self.request.user
        review.destination = destination
        
        # Check if it's a verified booking
        has_booking = Booking.objects.filter(
            user=self.request.user,
            destination=destination,
            status='confirmed'
        ).exists()
        review.is_verified_booking = has_booking
        
        review.save()
        
        # Update destination rating
        destination.update_rating()
        
        messages.success(self.request, 'Your review has been posted successfully!')
        return redirect('destinations:destination_detail', name=destination.name)


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update a review."""
    model = Review
    template_name = 'reviews/review_form.html'
    fields = ['rating', 'title', 'comment']
    login_url = 'users:login'
    
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user
    
    def handle_no_permission(self):
        messages.error(self.request, 'You cannot edit this review.')
        return redirect('destinations:destination_detail', name=self.get_object().destination.name)
    
    def form_valid(self, form):
        review = form.save()
        review.destination.update_rating()
        messages.success(self.request, 'Review updated successfully!')
        return redirect('destinations:destination_detail', name=review.destination.name)


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a review."""
    model = Review
    login_url = 'users:login'
    
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, 'You cannot delete this review.')
        return redirect('destinations:destination_detail', name=self.get_object().destination.name)
    
    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        destination = review.destination
        response = super().delete(request, *args, **kwargs)
        destination.update_rating()
        messages.success(request, 'Review deleted successfully!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('destinations:destination_detail', kwargs={'name': self.object.destination.name})
