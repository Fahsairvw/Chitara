import requests
import os
from .base import SongGeneratorStrategy


class SunoSongGenerator(SongGeneratorStrategy):
    """
    Suno AI implementation for real song generation.
    Calls the Suno API and returns a pending task ID for async processing.
    """

    def generate(self, data: dict) -> dict:
        """
        Generate a song using Suno API.
        
        Args:
            data (dict): Song generation parameters (title, genre, occasion)
            
        Returns:
            dict: Response with status and taskId for checking progress
        """

        api_key = os.getenv("SUNO_API_KEY")

        url = "https://api.sunoapi.org/api/v1/generate"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": data.get("title", "music"),
            "style": data.get("genre", "Pop"),
            "callBackUrl": "https://example.com/callback",
            "instrumental": False,
            "custom_mode": False,
            "model": "V3_5"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)

            print("SUNO STATUS:", response.status_code)
            print("SUNO RESPONSE:", response.text)

            if response.status_code != 200:
                return {
                    "status": "FAILED",
                    "taskId": None,
                    "url": None
                }

            response_data = response.json()

            task_id = response_data.get("data", {}).get("taskId")

            print("EXTRACTED TASK ID:", task_id)

            return {
                "status": "PENDING" if task_id else "FAILED",
                "taskId": task_id,
                "url": None
            }

        except Exception as e:
            return {
                "status": "FAILED",
                "taskId": None,
                "url": None,
                "error": str(e)
            }