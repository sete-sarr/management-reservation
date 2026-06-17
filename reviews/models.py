from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from destinations.models import Destination


class Review(models.Model):
    """Model representing user reviews for destinations."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='destination_reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_booking = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    unhelpful_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-helpful_count', '-created_at']
        verbose_name_plural = 'reviews'
        unique_together = ['user', 'destination']  # One review per user per destination
        indexes = [
            models.Index(fields=['destination', 'rating']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}'s review of {self.destination.name}"

    def get_rating_display(self):
        """Return star rating."""
        return '★' * self.rating + '☆' * (5 - self.rating)

    def mark_as_verified(self):
        """Mark review as verified purchase."""
        self.is_verified_booking = True
        self.save()

    def get_helpfulness_percentage(self):
        """Get percentage of reviews marked as helpful."""
        total = self.helpful_count + self.unhelpful_count
        if total == 0:
            return 0
        return (self.helpful_count / total) * 100
