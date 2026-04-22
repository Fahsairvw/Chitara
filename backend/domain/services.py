import time
import requests
import os
from .models import Song
from .models.choices import SongStatus
from .strategies.factory import get_generator_strategy
from django.conf import settings


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


def update_pending_songs():
    """Background task to check and update pending song statuses from Suno API"""
    while True:
        # Check both PENDING and GENERATING songs
        pending_songs = Song.objects.filter(status__in=[SongStatus.PENDING, SongStatus.GENERATING])

        for song in pending_songs:
            if not song.task_id:
                continue

            url = f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={song.task_id}"

            headers = {
                "Authorization": f"Bearer {os.getenv('SUNO_API_KEY')}"
            }

            try:
                response = requests.get(url, headers=headers)
                data = response.json()

                status = data.get("data", {}).get("status")

                if status == "SUCCESS":
                    suno_list = data.get("data", {}).get("response", {}).get("sunoData", [])

                    if len(suno_list) > 0:
                        audio_url = suno_list[0].get("audioUrl")

                        song.link = audio_url
                        song.status = SongStatus.SUCCEEDED
                        song.save()

                        print(f"Updated song {song.id}")

            except Exception as e:
                print("Error:", e)

        time.sleep(30)
