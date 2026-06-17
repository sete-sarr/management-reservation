from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from destinations.models import Destination


class Booking(models.Model):
    """Model representing a travel booking."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField(auto_now_add=True)
    travel_start_date = models.DateField()
    travel_end_date = models.DateField()
    number_of_people = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    payment_received = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booking_date']
        verbose_name_plural = 'bookings'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['destination', 'status']),
        ]

    def __str__(self):
        return f"Booking {self.confirmation_code} - {self.user.username}"

    def save(self, *args, **kwargs):
        """Generate confirmation code if not present."""
        if not self.confirmation_code:
            import uuid
            self.confirmation_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def get_price_breakdown(self):
        """Get price breakdown details."""
        return {
            'unit_price': self.destination.price_per_person,
            'number_of_people': self.number_of_people,
            'total_price': self.total_price,
        }

    def is_active(self):
        """Check if booking is currently active."""
        return self.status in ['confirmed', 'pending']

    def can_be_cancelled(self):
        """Check if booking can be cancelled."""
        from datetime import date
        return self.status in ['pending', 'confirmed'] and self.travel_start_date > date.today()
