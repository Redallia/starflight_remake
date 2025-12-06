# Planet Entity System - Architecture Analysis & Refactoring

## Current State Analysis

### What Works Well

1. **Deterministic Generation**: Uses seeds for consistent terrain/sensor data
2. **Separation of Concerns**: JSON data, terrain generation, sensor data are separate
3. **Perlin Noise System**: Sophisticated multi-layer terrain with seamless wrapping

### Current Architecture Issues

#### 1. **Planets Are Just Dictionaries**

Currently, planets are plain Python dicts loaded from JSON:

```python
{
    'name': 'Aqua',
    'coord_x': 15,
    'coord_y': 35,
    'radius': 4,
    'color': [80, 150, 220],
    'type': 'liquid',
    'seed': 2001,
    'terrain_params': {
        'has_surface': true,
        'water_coverage': 0.6,
        'elevation_scale': 0.3,
        'temperature': 0.5,
        'mineral_richness': 0.3
    }
}
```

**Problems:**
- No type safety or validation
- No encapsulation of planet behavior
- Planet-specific logic scattered across codebase
- Hard to extend with new planet types
- No clear interface for what a "planet" can do

#### 2. **Planet Type Logic is Scattered**

Planet type-specific behavior is spread across multiple files:

- **terrain_generator.py**: Has if/else for `gas_giant` vs other types (line 267)
- **sensor_data_generator.py**: Has templates for 5 planet types (magma, rocky, liquid, frozen, gas_giant)
- **star_systems.json**: Stores planet type as string
- **game_state.py**: Loads planets as dicts, no planet-specific logic

This means:
- Adding a new planet type requires changes in 3+ places
- Planet behavior isn't centralized
- Easy to create inconsistencies

#### 3. **No Planet Entity Layer**

There's no `Planet` class to encapsulate:
- Planet properties (mass, composition, atmosphere)
- Planet capabilities (can_land, has_atmosphere, is_scannable)
- Planet generation (terrain, sensor data)
- Planet rendering (colors, visual style)

#### 4. **Terrain Generation Hardcoded to Planet Types**

The terrain classification system (_classify_terrain) works only for Earth-like planets:
- Water/land distinction assumes liquid water
- Terrain types: deep_water, shallow_water, sand, grass, rock, mountain, mineral
- Gas giants get special color palette but same terrain types (doesn't make sense)
- No way to represent volcanic terrain, ice caps, frozen methane lakes, etc.

#### 5. **Missing Abstractions**

No clear entity hierarchy for:
- **Celestial Bodies**: Stars, planets, moons, starports, asteroids
- **Star Systems**: Collection of celestial bodies
- **Galaxy**: Collection of star systems

## Proposed Architecture

### Design Philosophy

**Composition over Inheritance (Like Crew System)**
- Base `CelestialBody` entity with common properties
- Planet types are configurations, not subclasses
- Use components/traits for planet capabilities

### Entity Hierarchy

```
entities/
├── celestial_body.py       # Base class for all space objects
├── star.py                 # Star entity (sun)
├── planet.py               # Planet entity with type-specific behavior
├── starport.py             # Starport entity (special celestial body)
└── star_system.py          # Star system entity (collection of bodies)

systems/
├── terrain_system.py       # Terrain generation (delegated by planet type)
├── sensor_system.py        # Sensor scanning logic
└── planet_loader.py        # Load planets from JSON into entities
```

### Core Components

#### 1. CelestialBody (Base Entity)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class CelestialBody(ABC):
    """Base class for all celestial objects"""
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
        """Can ship land on this body?"""
        pass

    @abstractmethod
    def is_scannable(self) -> bool:
        """Can sensors scan this body?"""
        pass
```

#### 2. Planet Entity

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class PlanetType(Enum):
    """Planet classification"""
    MAGMA = "magma"           # Volcanic, molten surface
    ROCKY = "rocky"           # Earth-like, rocky
    LIQUID = "liquid"         # Water world
    FROZEN = "frozen"         # Ice world
    GAS_GIANT = "gas_giant"   # Gas giant (no surface)

@dataclass
class TerrainParams:
    """Parameters for terrain generation"""
    has_surface: bool = True
    water_coverage: float = 0.3
    elevation_scale: float = 0.5
    temperature: float = 0.5
    mineral_richness: float = 0.2

    # Planet-type specific
    ice_coverage: float = 0.0      # For frozen worlds
    lava_coverage: float = 0.0     # For magma worlds
    atmospheric_turbulence: float = 0.5  # For gas giants

@dataclass
class Planet(CelestialBody):
    """Planet entity with type-specific behavior"""
    planet_type: PlanetType
    terrain_params: TerrainParams
    mass: Optional[int] = None  # Calculated from params if not set

    def can_orbit(self) -> bool:
        """All planets can be orbited"""
        return True

    def can_land(self) -> bool:
        """Can only land on planets with surfaces"""
        return self.terrain_params.has_surface

    def is_scannable(self) -> bool:
        """All non-starport planets can be scanned"""
        return True

    def get_terrain_generator(self):
        """Get appropriate terrain generator for this planet type"""
        from systems.terrain_system import get_terrain_generator
        return get_terrain_generator(self.planet_type, self)

    def get_sensor_data(self):
        """Generate sensor data for this planet"""
        from core.sensor_data_generator import generate_sensor_data
        # Pass entire planet entity instead of dict
        return generate_sensor_data(self)
```

#### 3. Star Entity

```python
from enum import Enum

class StarClass(Enum):
    """Stellar classification"""
    O = "O"  # Blue, very hot
    B = "B"  # Blue-white, hot
    A = "A"  # White, hot
    F = "F"  # Yellow-white, moderate
    G = "G"  # Yellow, moderate (like our Sun)
    K = "K"  # Orange, cool
    M = "M"  # Red, cool
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
        Get habitable zone distance range (in AU or coordinate units)
        Based on luminosity

        Returns:
            (inner_edge, outer_edge) in coordinate units
        """
        # Simplified: habitable zone scales with sqrt(luminosity)
        # For Sol (luminosity=1.0), habitable zone is ~0.95-1.37 AU
        inner = 0.95 * (self.luminosity ** 0.5)
        outer = 1.37 * (self.luminosity ** 0.5)
        return (inner, outer)
```

#### 4. Starport Entity

```python
@dataclass
class Starport(CelestialBody):
    """Space station / starport"""

    def can_orbit(self) -> bool:
        """Can't orbit starports"""
        return False

    def can_land(self) -> bool:
        """Can dock at starport"""
        return True

    def is_scannable(self) -> bool:
        """Can't scan starports"""
        return False
```

#### 5. StarSystem Entity

```python
@dataclass
class StarSystem:
    """Collection of celestial bodies in a star system"""
    name: str
    bodies: list[CelestialBody]

    def get_star(self) -> Optional[Star]:
        """Get primary star in system"""
        # In future, could support binary/multiple star systems
        return next((b for b in self.bodies if isinstance(b, Star)), None)

    def get_planets(self) -> list[Planet]:
        """Get all planets in system"""
        return [b for b in self.bodies if isinstance(b, Planet)]

    def get_starport(self) -> Optional[Starport]:
        """Get starport in system"""
        return next((b for b in self.bodies if isinstance(b, Starport)), None)

    def get_body_at(self, x: int, y: int) -> Optional[CelestialBody]:
        """Get celestial body at coordinates"""
        for body in self.bodies:
            # Check if coordinates are within body's radius
            dx = abs(body.coord_x - x)
            dy = abs(body.coord_y - y)
            distance = (dx**2 + dy**2) ** 0.5
            if distance <= body.radius:
                return body
        return None

    def is_in_habitable_zone(self, planet: Planet) -> bool:
        """Check if planet is in star's habitable zone"""
        star = self.get_star()
        if not star:
            return False

        # Calculate distance from star to planet
        dx = planet.coord_x - star.coord_x
        dy = planet.coord_y - star.coord_y
        distance = (dx**2 + dy**2) ** 0.5

        inner, outer = star.get_habitable_zone()
        return inner <= distance <= outer
```

### Terrain System Refactoring

#### Current Problem
`TerrainGenerator` has hardcoded logic for only 2 planet types (gas_giant vs everything else).

#### Solution: Strategy Pattern

```python
# systems/terrain_system.py

from abc import ABC, abstractmethod
from entities.planet import Planet, PlanetType

class TerrainStrategy(ABC):
    """Base class for planet-type-specific terrain generation"""

    @abstractmethod
    def classify_terrain(self, elevation: float, moisture: float,
                        has_mineral: bool, params: TerrainParams) -> str:
        """Classify terrain based on planet type"""
        pass

    @abstractmethod
    def get_terrain_colors(self) -> dict[str, tuple]:
        """Get color palette for this planet type"""
        pass

class RockyTerrainStrategy(TerrainStrategy):
    """Earth-like rocky planets"""

    def classify_terrain(self, elevation, moisture, has_mineral, params):
        # Current _classify_terrain logic
        water_level = params.water_coverage
        if elevation < water_level - 0.1:
            return 'deep_water'
        # ... etc

    def get_terrain_colors(self):
        return {
            'deep_water': (20, 50, 120),
            'shallow_water': (60, 100, 180),
            'sand': (210, 180, 140),
            # ... etc
        }

class FrozenTerrainStrategy(TerrainStrategy):
    """Frozen ice worlds"""

    def classify_terrain(self, elevation, moisture, has_mineral, params):
        ice_level = params.ice_coverage
        if elevation < ice_level - 0.1:
            return 'deep_ice'
        elif elevation < ice_level:
            return 'ice_shelf'
        elif has_mineral:
            return 'mineral'
        # ... ice-specific terrain types

    def get_terrain_colors(self):
        return {
            'deep_ice': (180, 200, 230),
            'ice_shelf': (200, 220, 240),
            'frozen_rock': (120, 130, 150),
            # ... etc
        }

class MagmaTerrainStrategy(TerrainStrategy):
    """Volcanic molten worlds"""

    def classify_terrain(self, elevation, moisture, has_mineral, params):
        lava_level = params.lava_coverage
        if elevation < lava_level:
            return 'lava_ocean'
        elif elevation < lava_level + 0.1:
            return 'volcanic_crust'
        # ... volcanic terrain types

    def get_terrain_colors(self):
        return {
            'lava_ocean': (200, 50, 20),
            'volcanic_crust': (80, 40, 30),
            # ... etc
        }

class GasGiantTerrainStrategy(TerrainStrategy):
    """Gas giants - atmospheric bands"""

    def classify_terrain(self, elevation, moisture, has_mineral, params):
        # Gas giants don't have traditional terrain
        # Use elevation to represent atmospheric bands/zones
        if elevation < 0.2:
            return 'deep_atmosphere'
        elif elevation < 0.4:
            return 'storm_band'
        # ... atmospheric zones

    def get_terrain_colors(self):
        return {
            'deep_atmosphere': (80, 40, 100),
            'storm_band': (120, 60, 140),
            # ... purple/pink palette
        }

# Factory function
def get_terrain_strategy(planet_type: PlanetType) -> TerrainStrategy:
    """Get terrain strategy for planet type"""
    strategies = {
        PlanetType.ROCKY: RockyTerrainStrategy(),
        PlanetType.LIQUID: RockyTerrainStrategy(),  # Same as rocky
        PlanetType.FROZEN: FrozenTerrainStrategy(),
        PlanetType.MAGMA: MagmaTerrainStrategy(),
        PlanetType.GAS_GIANT: GasGiantTerrainStrategy(),
    }
    return strategies.get(planet_type, RockyTerrainStrategy())
```

### Migration Strategy

#### Phase 1: Create Entity Classes (Non-Breaking)

1. Create `entities/celestial_body.py`, `planet.py`, `starport.py`, `star_system.py`
2. Create `systems/planet_loader.py` to convert JSON → entities
3. Keep backward compatibility - entities can export to dict format

#### Phase 2: Update GameState

4. Change `GameState.planets` from `list[dict]` to `list[CelestialBody]`
5. Update `_load_system_data()` to use PlanetLoader
6. Update `orbiting_planet` to be `Optional[Planet]` instead of `Optional[dict]`

#### Phase 3: Update Dependent Systems

7. Update `TerrainGenerator` to accept `Planet` entity instead of dict
8. Update `sensor_data_generator` to accept `Planet` entity
9. Update screens that access planet data

#### Phase 4: Refactor Terrain System (Optional Enhancement)

10. Extract terrain strategies for each planet type
11. Support new terrain types per planet type
12. Improve visual variety

## Benefits of Refactoring

### 1. Type Safety
```python
# Before (no type checking)
planet = {'name': 'Aqua', 'type': 'watr'}  # Typo not caught
if planet['type'] == 'gas_giant':  # String comparison everywhere

# After (type-safe)
planet = Planet(name='Aqua', planet_type=PlanetType.GAS_GIANT)
if planet.planet_type == PlanetType.GAS_GIANT:  # Enum comparison
```

### 2. Clear Capabilities
```python
# Before (implicit knowledge)
if planet.get('terrain_params', {}).get('has_surface'):
    # Can we land? Not clear from dict structure

# After (explicit interface)
if planet.can_land():  # Clear and encapsulated
```

### 3. Easy Extension
```python
# Adding new planet type:
# Before: Modify JSON, terrain_generator.py, sensor_data_generator.py, etc.

# After:
# 1. Add to PlanetType enum
# 2. Create terrain strategy class
# 3. Add to sensor templates
# All in one place, clear extension points
```

### 4. Better Planet Behaviors
```python
# Can add planet-specific methods easily:
class Planet:
    def get_gravity(self) -> float:
        """Calculate surface gravity"""
        return self.mass / (self.radius ** 2)

    def get_atmosphere_density(self) -> float:
        """Get atmospheric density for landing difficulty"""
        # Use sensor data to calculate
        pass

    def has_life(self) -> bool:
        """Check if planet has biological life"""
        sensor_data = self.get_sensor_data()
        return sensor_data.bio_density > 0
```

### 5. Cleaner Star System Management
```python
# Before
starport = next((p for p in game_state.planets if p['type'] == 'starport'), None)

# After
starport = game_state.current_star_system.get_starport()
```

## Design Decisions

### Star System Scope (Initial Implementation)

1. **Star Placement**: Stars positioned at center of coordinate grid (25, 25)
   - Simplifies initial implementation
   - Matches typical star system layout
   - Can add orbital mechanics later if needed

2. **Binary/Multiple Star Systems**: Not supported initially
   - Original Starflight didn't have binary stars
   - Keep implementation simple for now
   - Design allows for future extension (see `get_star()` comment)

3. **Star Scanning Data**: Informational only
   - Spectral class, temperature, luminosity, age, solar activity, radiation levels
   - No immediate gameplay effects
   - Placeholder data until specific interface points are developed

4. **Star Effects on Gameplay**: Deferred for later
   - Proximity to star doesn't affect fuel efficiency, radiation damage, or sensors
   - Original game didn't emphasize these mechanics
   - Can be interesting future enhancement, but not critical now

### Future Considerations

1. **Should we support moons?**
   - Moons could be `CelestialBody` that orbit planets
   - Would need orbital mechanics or simplified parent/child relationship

2. **Procedural planet generation?**
   - Currently all planets in JSON
   - Could generate random planets for exploration
   - Would need `PlanetGenerator` system

3. **Planet state/changes over time?**
   - Mining depletes minerals
   - Terraform changes atmosphere
   - Would need mutable planet state vs immutable template

4. **Multiple star systems?**
   - Current: Single system loaded
   - Future: Galaxy with many systems
   - Need galaxy/sector management

## Recommendation

**Start with Phase 1-3**: Create entity layer without breaking existing code, then migrate gradually. This provides immediate benefits (type safety, encapsulation) without requiring a full rewrite.

**Phase 4 (terrain strategies)** can be deferred - it's an enhancement, not critical architecture.

**Don't over-engineer early**: Focus on current needs (single system, 5 planet types), design for extensibility but don't implement features we don't need yet.
