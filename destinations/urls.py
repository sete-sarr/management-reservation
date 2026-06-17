from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('browse/', views.DestinationListView.as_view(), name='destination_list'),
    path('<str:name>/', views.DestinationDetailView.as_view(), name='destination_detail'),
]
