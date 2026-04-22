from django.conf import settings
from .base import SongGeneratorStrategy
from .mock import MockSongGenerator
from .suno import SunoSongGenerator


def get_generator_strategy() -> SongGeneratorStrategy:
    if settings.GENERATOR_STRATEGY == "suno":
        return SunoSongGenerator()

    return MockSongGenerator()
