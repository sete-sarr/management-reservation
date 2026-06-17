from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Destination
from reviews.models import Review
from bookings.models import Booking


class DestinationListView(ListView):
    """View to display list of all destinations with search and filter."""
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 12

    def get_queryset(self):
        queryset = Destination.objects.filter(is_active=True).annotate(
            avg_rating=Avg('destination_reviews__rating'),
            review_count=Count('destination_reviews')
        )
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(country__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by country
        country = self.request.GET.get('country', '')
        if country:
            queryset = queryset.filter(country=country)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        if min_price:
            queryset = queryset.filter(price_per_person__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_person__lte=max_price)
        
        # Filter by rating
        rating_filter = self.request.GET.get('rating', '')
        if rating_filter:
            queryset = queryset.filter(rating__gte=rating_filter)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-is_featured')
        if sort_by in ['price_asc', 'price_desc', 'rating', 'reviews']:
            if sort_by == 'price_asc':
                queryset = queryset.order_by('price_per_person')
            elif sort_by == 'price_desc':
                queryset = queryset.order_by('-price_per_person')
            elif sort_by == 'rating':
                queryset = queryset.order_by('-rating')
            elif sort_by == 'reviews':
                queryset = queryset.order_by('-reviews_count')
        else:
            queryset = queryset.order_by('-is_featured', '-rating', '-reviews_count')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique countries for filter
        context['countries'] = Destination.objects.values_list('country', flat=True).distinct()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_country'] = self.request.GET.get('country', '')
        return context


def home_view(request):
    """Home page showing featured destinations."""
    featured_destinations = Destination.objects.filter(
        is_active=True,
        is_featured=True
    ).annotate(
        avg_rating=Avg('destination_reviews__rating')
    )[:8]
    
    popular_destinations = Destination.objects.filter(
        is_active=True
    ).annotate(
        avg_rating=Avg('destination_reviews__rating'),
        review_count=Count('destination_reviews')
    ).order_by('-reviews_count')[:8]
    
    context = {
        'featured': featured_destinations,
        'popular': popular_destinations,
        'total_destinations': Destination.objects.filter(is_active=True).count(),
        'total_bookings': Booking.objects.filter(status='confirmed').count(),
    }
    return render(request, 'destinations/home.html', context)


class DestinationDetailView(DetailView):
    """View to display detailed information about a specific destination."""
    model = Destination
    template_name = 'destinations/destination_detail.html'
    context_object_name = 'destination'
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Destination, name=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.get_object()
        
        # Get reviews
        context['reviews'] = Review.objects.filter(
            destination=destination
        ).order_by('-is_featured', '-helpful_count', '-created_at')[:10]
        
        # Get rating breakdown
        reviews_qs = Review.objects.filter(destination=destination)
        rating_breakdown = {}
        for i in range(1, 6):
            rating_breakdown[i] = reviews_qs.filter(rating=i).count()
        context['rating_breakdown'] = rating_breakdown
        context['total_reviews'] = reviews_qs.count()
        context['available_remaining'] = destination.get_available_remaining()
        
        return context
