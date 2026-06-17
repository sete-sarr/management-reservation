from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['confirmation_code', 'get_username', 'destination', 'travel_start_date', 'number_of_people', 'total_price', 'status', 'payment_received', 'booking_date']
    list_filter = ['status', 'payment_received', 'booking_date', 'destination']
    search_fields = ['confirmation_code', 'user__username', 'destination__name']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('confirmation_code', 'user', 'destination')
        }),
        ('Travel Details', {
            'fields': ('travel_start_date', 'travel_end_date', 'number_of_people')
        }),
        ('Pricing & Payment', {
            'fields': ('total_price', 'payment_received', 'status')
        }),
        ('Additional Information', {
            'fields': ('special_requests',)
        }),
        ('Timestamps', {
            'fields': ('booking_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['confirmation_code', 'booking_date', 'created_at', 'updated_at']
    
    actions = ['confirm_booking', 'cancel_booking', 'mark_payment_received', 'mark_payment_pending']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Customer'
    
    def confirm_booking(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, "Selected bookings confirmed.")
    confirm_booking.short_description = "Confirm selected bookings"
    
    def cancel_booking(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, "Selected bookings cancelled.")
    cancel_booking.short_description = "Cancel selected bookings"
    
    def mark_payment_received(self, request, queryset):
        queryset.update(payment_received=True)
        self.message_user(request, "Payments marked as received.")
    mark_payment_received.short_description = "Mark payment as received"
    
    def mark_payment_pending(self, request, queryset):
        queryset.update(payment_received=False)
        self.message_user(request, "Payments marked as pending.")
    mark_payment_pending.short_description = "Mark payment as pending"
