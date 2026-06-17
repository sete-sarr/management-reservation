from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'get_full_name', 'role', 'phone', 'city', 'country', 'is_verified', 'total_bookings', 'created_at']
    list_filter = ['role', 'is_verified', 'created_at', 'country']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone', 'city']
    
    fieldsets = (
        ('User Account', {
            'fields': ('user', 'role')
        }),
        ('Personal Information', {
            'fields': ('phone', 'date_of_birth', 'bio', 'profile_picture')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Statistics', {
            'fields': ('total_bookings', 'total_spent', 'is_verified'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'total_bookings', 'total_spent']
    
    actions = ['verify_users', 'unverify_users', 'make_admin', 'make_customer']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'
    
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, "Selected users verified.")
    verify_users.short_description = "Mark selected users as verified"
    
    def unverify_users(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, "Selected users unverified.")
    unverify_users.short_description = "Mark selected users as unverified"
    
    def make_admin(self, request, queryset):
        queryset.update(role='admin')
        self.message_user(request, "Selected users made administrators.")
    make_admin.short_description = "Make selected users administrators"
    
    def make_customer(self, request, queryset):
        queryset.update(role='customer')
        self.message_user(request, "Selected users made customers.")
    make_customer.short_description = "Make selected users customers"
