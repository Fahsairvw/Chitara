class MockSongGenerator:

    def generate(self, data):
        return {
            "status": "Succeeded",
            "url": "https://example.com/mock-song.mp3",
            "taskId": None
        }
