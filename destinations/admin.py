from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'price_per_person', 'available_slots', 'rating', 'reviews_count', 'is_featured', 'is_active']
    list_filter = ['country', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'country', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'country', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price_per_person', 'available_slots', 'duration_days')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Ratings & Reviews', {
            'fields': ('rating', 'reviews_count'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['rating', 'reviews_count', 'created_at', 'updated_at']
    
    actions = ['mark_featured', 'unmark_featured', 'activate', 'deactivate']
    
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, "Selected destinations marked as featured.")
    mark_featured.short_description = "Mark selected as featured"
    
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, "Selected destinations unmarked as featured.")
    unmark_featured.short_description = "Unmark selected as featured"
    
    def activate(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected destinations activated.")
    activate.short_description = "Activate selected destinations"
    
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected destinations deactivated.")
    deactivate.short_description = "Deactivate selected destinations"
