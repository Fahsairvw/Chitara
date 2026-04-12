from .models import Song
from .strategies.factory import get_generator_strategy
from django.conf import settings
print("STRATEGY:", settings.GENERATOR_STRATEGY)


class MusicService:

    def generate_song(self, user, library, data):

        strategy = get_generator_strategy()

        result = strategy.generate(data)

        song = Song.objects.create(
            title=data["title"],
            genre=data["genre"],
            occasion=data["occasion"],
            user=user,
            library=library,
            status=result.get("status"),
            link=result.get("url"),   
            task_id=result.get("taskId")
        )

        return song, result
