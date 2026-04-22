from abc import ABC, abstractmethod


class SongGeneratorStrategy(ABC):
    """
    Abstract Base Class defining the interface for song generation strategies.
    
    All concrete song generator implementations must inherit from this class
    and implement the generate method.
    """

    @abstractmethod
    def generate(self, data: dict) -> dict:
        """
        Generate a song based on the provided data.

        Args:
            data (dict): Configuration data for song generation containing:
                - title: Song title/prompt
                - genre: Music genre
                - occasion: Occasion for the song
                - Any other strategy-specific parameters

        Returns:
            dict: Response containing:
                - status: "PENDING", "Succeeded", or "FAILED"
                - taskId: Unique task identifier (for async operations)
                - url: Direct URL to generated song (if available)
                - error: Error message (if status is "FAILED")
        """
        pass
