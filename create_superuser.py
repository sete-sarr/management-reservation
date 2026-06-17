import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management_reservation.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

# Create superuser
try:
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser('admin', 'admin@travelhub.com', 'admin@123')
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.role = 'admin'
        profile.save()
        print("✓ Superuser 'admin' created successfully!")
        print("  Username: admin")
        print("  Email: admin@travelhub.com")
        print("  Password: admin@123")
    else:
        print("✓ Admin user already exists")
except Exception as e:
    print(f"✗ Error creating superuser: {e}")
