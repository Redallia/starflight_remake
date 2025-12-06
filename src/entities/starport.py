"""
Starport entity (space station)
"""
from dataclasses import dataclass
from entities.celestial_body import CelestialBody


@dataclass
class Starport(CelestialBody):
    """Space station / starport where player can dock"""

    def can_orbit(self) -> bool:
        """Can't orbit starports"""
        return False

    def can_land(self) -> bool:
        """Can dock at starport"""
        return True

    def is_scannable(self) -> bool:
        """Can't scan starports"""
        return False

    def to_dict(self) -> dict:
        """Convert to dictionary format for backward compatibility"""
        base_dict = super().to_dict()
        base_dict.update({
            'type': 'starport',
            'terrain_params': {
                'has_surface': False
            }
        })
        return base_dict

    @staticmethod
    def from_dict(data: dict) -> 'Starport':
        """Create Starport from dictionary"""
        return Starport(
            name=data['name'],
            coord_x=data['coord_x'],
            coord_y=data['coord_y'],
            radius=data['radius'],
            color=tuple(data['color']) if isinstance(data['color'], list) else data['color'],
            seed=data['seed'],
        )
