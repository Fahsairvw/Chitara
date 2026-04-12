from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.users),
    path("libraries/", views.libraries),
    path("songs/", views.songs),
    path("songs/<int:pk>/", views.song_detail),
    path('songs/generate/', views.create_song),
    path('songs/status/<str:task_id>/', views.check_song),
]