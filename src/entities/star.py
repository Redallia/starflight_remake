"""
Star entity (sun)
"""
from enum import Enum
from dataclasses import dataclass
from entities.celestial_body import CelestialBody


class StarClass(Enum):
    """Stellar classification (OBAFGKM spectral types)"""
    O = "O"  # Blue, very hot (30,000+ K)
    B = "B"  # Blue-white, hot (10,000-30,000 K)
    A = "A"  # White, hot (7,500-10,000 K)
    F = "F"  # Yellow-white, moderate (6,000-7,500 K)
    G = "G"  # Yellow, moderate (5,200-6,000 K) - like our Sun
    K = "K"  # Orange, cool (3,700-5,200 K)
    M = "M"  # Red, cool (2,400-3,700 K)
    # Could add: L, T (brown dwarfs), D (white dwarfs), etc.


@dataclass
class Star(CelestialBody):
    """Star entity (sun)"""
    star_class: StarClass
    temperature: int  # Kelvin
    luminosity: float  # Relative to Sol (1.0 = Sun-like)

    def can_orbit(self) -> bool:
        """Can't orbit stars (too dangerous)"""
        return False

    def can_land(self) -> bool:
        """Can't land on stars"""
        return False

    def is_scannable(self) -> bool:
        """Stars can be scanned for spectral analysis"""
        return True

    def get_color(self) -> tuple[int, int, int]:
        """Get star color based on stellar class"""
        # Override the color from base class with temperature-based color
        colors = {
            StarClass.O: (150, 180, 255),  # Blue
            StarClass.B: (180, 200, 255),  # Blue-white
            StarClass.A: (220, 220, 255),  # White
            StarClass.F: (255, 255, 220),  # Yellow-white
            StarClass.G: (255, 255, 200),  # Yellow (Sun-like)
            StarClass.K: (255, 200, 150),  # Orange
            StarClass.M: (255, 150, 100),  # Red
        }
        return colors.get(self.star_class, (255, 255, 255))

    def get_habitable_zone(self) -> tuple[float, float]:
        """
        Get habitable zone distance range (in coordinate units)
        Based on luminosity

        Returns:
            (inner_edge, outer_edge) in coordinate units
        """
        # Simplified: habitable zone scales with sqrt(luminosity)
        # For Sol (luminosity=1.0), habitable zone is ~0.95-1.37 AU
        inner = 0.95 * (self.luminosity ** 0.5)
        outer = 1.37 * (self.luminosity ** 0.5)
        return (inner, outer)

    def to_dict(self) -> dict:
        """Convert to dictionary format for backward compatibility"""
        base_dict = super().to_dict()
        base_dict.update({
            'type': 'star',
            'star_class': self.star_class.value,
            'temperature': self.temperature,
            'luminosity': self.luminosity,
        })
        return base_dict
