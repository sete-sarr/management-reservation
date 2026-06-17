from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'get_booking_code', 'amount', 'payment_method', 'payment_status', 'payment_date', 'created_at']
    list_filter = ['payment_method', 'payment_status', 'payment_date', 'created_at']
    search_fields = ['transaction_id', 'booking__confirmation_code', 'booking__user__username']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('booking', 'transaction_id', 'payment_method')
        }),
        ('Amount Details', {
            'fields': ('amount', 'refund_amount')
        }),
        ('Status', {
            'fields': ('payment_status', 'payment_date', 'refund_date')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['mark_completed', 'mark_failed', 'mark_refunded']
    
    def get_booking_code(self, obj):
        return obj.booking.confirmation_code
    get_booking_code.short_description = 'Booking Code'
    
    def mark_completed(self, request, queryset):
        queryset.update(payment_status='completed')
        self.message_user(request, "Payments marked as completed.")
    mark_completed.short_description = "Mark as completed"
    
    def mark_failed(self, request, queryset):
        queryset.update(payment_status='failed')
        self.message_user(request, "Payments marked as failed.")
    mark_failed.short_description = "Mark as failed"
    
    def mark_refunded(self, request, queryset):
        queryset.update(payment_status='refunded')
        self.message_user(request, "Payments marked as refunded.")
    mark_refunded.short_description = "Mark as refunded"
