from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_username', 'destination', 'rating', 'get_rating_display', 'is_verified_booking', 'helpful_count', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_verified_booking', 'created_at']
    search_fields = ['title', 'comment', 'user__username', 'destination__name']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'destination', 'title', 'comment')
        }),
        ('Rating', {
            'fields': ('rating',)
        }),
        ('Verification & Status', {
            'fields': ('is_verified_booking', 'is_featured')
        }),
        ('Engagement', {
            'fields': ('helpful_count', 'unhelpful_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['mark_featured', 'unmark_featured', 'verify_reviews', 'unverify_reviews']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Reviewer'
    
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, "Selected reviews marked as featured.")
    mark_featured.short_description = "Mark as featured"
    
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, "Selected reviews unmarked as featured.")
    unmark_featured.short_description = "Unmark as featured"
    
    def verify_reviews(self, request, queryset):
        queryset.update(is_verified_booking=True)
        self.message_user(request, "Selected reviews marked as verified purchases.")
    verify_reviews.short_description = "Mark as verified purchases"
    
    def unverify_reviews(self, request, queryset):
        queryset.update(is_verified_booking=False)
        self.message_user(request, "Selected reviews marked as unverified.")
    unverify_reviews.short_description = "Mark as unverified"
