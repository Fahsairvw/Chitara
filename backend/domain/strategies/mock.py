from .base import SongGeneratorStrategy


class MockSongGenerator(SongGeneratorStrategy):
    """
    Mock implementation for testing and development.
    Returns fake instant response without calling external APIs.
    """

    def generate(self, data: dict) -> dict:
        """
        Generate a mock song instantly.
        
        Args:
            data (dict): Song generation parameters
            
        Returns:
            dict: Mock song response with immediate success status
        """
        return {
            "status": "Succeeded",
            "url": "https://example.com/mock-song.mp3",
            "taskId": None
        }
