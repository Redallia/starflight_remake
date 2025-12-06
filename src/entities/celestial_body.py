"""
Base class for all celestial objects (stars, planets, starports)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CelestialBody(ABC):
    """Base class for all celestial objects in the game"""
    name: str
    coord_x: int
    coord_y: int
    radius: int
    color: tuple[int, int, int]
    seed: int

    @abstractmethod
    def can_orbit(self) -> bool:
        """Can ship enter orbit around this body?"""
        pass

    @abstractmethod
    def can_land(self) -> bool:
        """Can ship land on/dock with this body?"""
        pass

    @abstractmethod
    def is_scannable(self) -> bool:
        """Can sensors scan this body?"""
        pass

    def to_dict(self) -> dict:
        """
        Convert entity to dictionary format for backward compatibility

        Returns:
            Dictionary representation compatible with existing code
        """
        return {
            'name': self.name,
            'coord_x': self.coord_x,
            'coord_y': self.coord_y,
            'radius': self.radius,
            'color': self.color,
            'seed': self.seed,
        }
