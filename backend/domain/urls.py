from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.users),
    path("libraries/", views.libraries),
    path("songs/", views.songs),
    path("songs/<int:pk>/", views.song_detail),
    path('songs/generate/', views.create_song),
    path('songs/status/<str:task_id>/', views.check_song),
    path('choices/', views.choices),
    # Google OAuth endpoints
    path('auth/google/', views.google_oauth_start),
    path('auth/google/callback/', views.google_oauth_callback),
    path('auth/google/token/', views.google_auth),
]