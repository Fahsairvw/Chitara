from django.db import models


class UserRole(models.TextChoices):
    PLATFORM_OWNER = "PlatformOwner", "Platform Owner"
    USER = "User", "User"


class Genre(models.TextChoices):
    POP = "Pop", "Pop"
    ROCK = "Rock", "Rock"
    CLASSICAL = "Classical", "Classical"
    JAZZ = "Jazz", "Jazz"
    RANDB = "RandB", "R&B"
    COUNTRY = "Country", "Country"


class SongStatus(models.TextChoices):
    GENERATING = "Generating", "Generating"
    SUCCEEDED = "Succeeded", "Succeeded"
    FAILED = "Failed", "Failed"


class Occasion(models.TextChoices):
    PARTY = "Party", "Party"
    STUDY = "Study", "Study"
    RELAX = "Relax", "Relax"
    WORK = "Work", "Work"
    WORKOUT = "Workout", "Workout"
    SLEEP = "Sleep", "Sleep"
