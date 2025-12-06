"""
Planet entity with type-specific behavior
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from entities.celestial_body import CelestialBody


class PlanetType(Enum):
    """Planet classification"""
    MAGMA = "magma"           # Volcanic, molten surface
    ROCKY = "rocky"           # Earth-like, rocky
    LIQUID = "liquid"         # Water world
    FROZEN = "frozen"         # Ice world
    GAS_GIANT = "gas_giant"   # Gas giant (no solid surface)


@dataclass
class TerrainParams:
    """Parameters for terrain generation"""
    has_surface: bool = True
    water_coverage: float = 0.3
    elevation_scale: float = 0.5
    temperature: float = 0.5
    mineral_richness: float = 0.2

    # Planet-type specific parameters
    ice_coverage: float = 0.0      # For frozen worlds
    lava_coverage: float = 0.0     # For magma worlds
    atmospheric_turbulence: float = 0.5  # For gas giants

    @staticmethod
    def from_dict(data: dict) -> 'TerrainParams':
        """Create TerrainParams from dictionary"""
        return TerrainParams(
            has_surface=data.get('has_surface', True),
            water_coverage=data.get('water_coverage', 0.3),
            elevation_scale=data.get('elevation_scale', 0.5),
            temperature=data.get('temperature', 0.5),
            mineral_richness=data.get('mineral_richness', 0.2),
            ice_coverage=data.get('ice_coverage', 0.0),
            lava_coverage=data.get('lava_coverage', 0.0),
            atmospheric_turbulence=data.get('atmospheric_turbulence', 0.5),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary format"""
        return {
            'has_surface': self.has_surface,
            'water_coverage': self.water_coverage,
            'elevation_scale': self.elevation_scale,
            'temperature': self.temperature,
            'mineral_richness': self.mineral_richness,
            'ice_coverage': self.ice_coverage,
            'lava_coverage': self.lava_coverage,
            'atmospheric_turbulence': self.atmospheric_turbulence,
        }


@dataclass
class Planet(CelestialBody):
    """Planet entity with type-specific behavior"""
    planet_type: PlanetType
    terrain_params: TerrainParams = field(default_factory=TerrainParams)
    mass: Optional[int] = None  # Calculated from params if not set

    def can_orbit(self) -> bool:
        """All planets can be orbited"""
        return True

    def can_land(self) -> bool:
        """Can only land on planets with surfaces"""
        return self.terrain_params.has_surface

    def is_scannable(self) -> bool:
        """All planets can be scanned"""
        return True

    def get_terrain_generator(self):
        """Get appropriate terrain generator for this planet type"""
        from core.terrain_generator import TerrainGenerator
        # Pass the planet's to_dict() for backward compatibility
        return TerrainGenerator(self.to_dict())

    def get_sensor_data(self):
        """Generate sensor data for this planet"""
        from core.sensor_data_generator import generate_sensor_data
        # Pass the planet's to_dict() for backward compatibility
        return generate_sensor_data(self.to_dict())

    def to_dict(self) -> dict:
        """Convert to dictionary format for backward compatibility"""
        base_dict = super().to_dict()
        base_dict.update({
            'type': self.planet_type.value,
            'terrain_params': self.terrain_params.to_dict(),
        })
        if self.mass is not None:
            base_dict['mass'] = self.mass
        return base_dict

    @staticmethod
    def from_dict(data: dict) -> 'Planet':
        """Create Planet from dictionary"""
        planet_type = PlanetType(data['type'])
        terrain_params = TerrainParams.from_dict(data.get('terrain_params', {}))

        return Planet(
            name=data['name'],
            coord_x=data['coord_x'],
            coord_y=data['coord_y'],
            radius=data['radius'],
            color=tuple(data['color']) if isinstance(data['color'], list) else data['color'],
            seed=data['seed'],
            planet_type=planet_type,
            terrain_params=terrain_params,
            mass=data.get('mass'),
        )
