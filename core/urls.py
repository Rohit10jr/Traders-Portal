from django.urls import path
from .views import RegisterView, Home, CompanyListCreateView, CompanyDetailView, WatchlistListCreateView, WatchlistListDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', Home.as_view(), name='Home'),

    # Company CRUD + search
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    # Watchlist CRUD (User-specific)
    path('watchlist/', WatchlistListCreateView.as_view(), name='watchlist-list-create'),
    path('watchlist/<int:pk>/', WatchlistListDetailView.as_view(), name='watchlist-detail')
]