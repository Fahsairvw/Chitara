from django.db import models


class UserRole(models.TextChoices):
    PLATFORM_OWNER = "PlatformOwner", "Platform Owner"
    USER = "User", "User"


class Genre(models.TextChoices):
    POP = "Pop", "Pop"
    ROCK = "Rock", "Rock"
    CLASSICAL = "Classical", "Classical"


class SongStatus(models.TextChoices):
    GENERATING = "Generating", "Generating"
    SUCCEEDED = "Succeeded", "Succeeded"
    FAILED = "Failed", "Failed"


class Occasion(models.TextChoices):
    PARTY = "Party", "Party"
    STUDY = "Study", "Study"
    RELAX = "Relax", "Relax"


class User(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Library(models.Model):
    name = models.CharField(max_length=200)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="library"
    )

    def __str__(self):
        return self.name


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
