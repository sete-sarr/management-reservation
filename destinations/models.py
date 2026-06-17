from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Destination(models.Model):
    """Model representing a travel destination."""
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100)
    description = models.TextField()
    price_per_person = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    available_slots = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    duration_days = models.IntegerField(default=5)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    reviews_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-rating', '-reviews_count']
        verbose_name_plural = 'destinations'
        indexes = [
            models.Index(fields=['country', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} - {self.country}"

    def get_average_rating(self):
        """Calculate the average rating from reviews."""
        from reviews.models import Review
        reviews = Review.objects.filter(destination=self)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0

    def update_rating(self):
        """Update the destination rating and review count."""
        avg_rating = self.get_average_rating()
        if avg_rating:
            self.rating = round(avg_rating, 1)
        from reviews.models import Review
        self.reviews_count = Review.objects.filter(destination=self).count()
        self.save()

    def get_booked_slots(self):
        """Get the number of booked slots."""
        from bookings.models import Booking
        booked = Booking.objects.filter(
            destination=self, 
            status='confirmed'
        ).aggregate(total=models.Sum('number_of_people'))['total'] or 0
        return booked

    def get_available_remaining(self):
        """Get the remaining available slots."""
        return max(0, self.available_slots - self.get_booked_slots())
