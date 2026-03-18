from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.users),
    path("libraries/", views.libraries),
    path("songs/", views.songs),
    path("songs/<int:pk>/", views.song_detail),
]