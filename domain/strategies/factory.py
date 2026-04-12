from django.conf import settings
from .mock import MockSongGenerator
from .suno import SunoSongGenerator


def get_generator_strategy():

    if settings.GENERATOR_STRATEGY == "suno":
        return SunoSongGenerator()

    return MockSongGenerator()
