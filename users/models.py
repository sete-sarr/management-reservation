from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    """Extended user profile model."""
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[RegexValidator(r'^\d{10,}$', 'Enter a valid phone number')]
    )
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default.png')
    bio = models.TextField(blank=True, max_length=500)
    is_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=True, null=True)
    total_bookings = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'user profiles'

    def __str__(self):
        return f"{self.user.first_name or self.user.username}'s Profile"

    def get_full_address(self):
        """Return complete address."""
        parts = filter(None, [self.address, self.city, self.country, self.postal_code])
        return ', '.join(parts)

    def is_admin_user(self):
        return self.role == 'admin' or self.user.is_superuser

    def is_customer(self):
        return self.role == 'customer'
