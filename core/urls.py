from django.urls import path
from .views import RegisterView, Home,CompanyListView, UserWatchListView, AddToWatchlistView, RemoveFromWatchlistView,CompanyListCreateView, CompanyDetailView, WatchlistListCreateView, WatchlistListDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', Home.as_view(), name='Home'),
    path('company/', CompanyListView.as_view(), name='company-list'),
    path('watch/', UserWatchListView.as_view(), name='user-watchlist'),
    path('watch/add/', AddToWatchlistView.as_view(), name='add-watchlist'),
    path('watch/remove/<int:pk>/', RemoveFromWatchlistView.as_view(), name='remove-watchlist'),

    # Company CRUD + search
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    # Watchlist CRUD (User-specific)
    path('watchlist/', WatchlistListCreateView.as_view(), name='watchlist-list-create'),
    path('watchlist/<int:pk>/', WatchlistListDetailView.as_view(), name='watchlist-detail')
]