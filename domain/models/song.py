from django.db import models
from .choices import SongStatus, Genre, Occasion
from .library import Library
from .user import User


class Song(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)

    description = models.TextField(blank=True)

    createAt = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=SongStatus.choices,
        default=SongStatus.GENERATING
    )

    genre = models.CharField(
        max_length=20,
        choices=Genre.choices
    )

    occasion = models.CharField(
        max_length=20,
        choices=Occasion.choices
    )

    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name="songs"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="generated_songs"
    )

    def __str__(self):
        return self.title
