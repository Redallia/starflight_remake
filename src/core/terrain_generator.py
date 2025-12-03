"""
Terrain generation system using Perlin noise
Generates consistent, deterministic planetary surfaces
"""
from noise import pnoise2


class TerrainType:
    """Terrain type constants"""
    DEEP_WATER = 'deep_water'
    SHALLOW_WATER = 'shallow_water'
    SAND = 'sand'
    GRASS = 'grass'
    ROCK = 'rock'
    MOUNTAIN = 'mountain'
    MINERAL = 'mineral'


class TerrainGenerator:
    """Generates terrain using Perlin noise with layered maps"""

    def __init__(self, planet_data):
        """
        Initialize terrain generator for a planet

        Args:
            planet_data: Planet dictionary with seed and terrain_params
        """
        self.planet_data = planet_data
        self.seed = planet_data.get('seed', 0)
        self.params = planet_data.get('terrain_params', {})

        # Default terrain parameters
        self.water_coverage = self.params.get('water_coverage', 0.3)
        self.elevation_scale = self.params.get('elevation_scale', 0.5)
        self.temperature = self.params.get('temperature', 0.5)
        self.mineral_richness = self.params.get('mineral_richness', 0.2)

    def generate(self, width, height):
        """
        Generate terrain grid

        Args:
            width: Grid width
            height: Grid height

        Returns:
            2D list of terrain types
        """
        # Generate multiple noise layers
        elevation_map = self._generate_elevation_map(width, height)
        moisture_map = self._generate_moisture_map(width, height)
        mineral_map = self._generate_mineral_map(width, height)

        # Combine layers to determine terrain
        terrain = []
        for y in range(height):
            row = []
            for x in range(width):
                elevation = elevation_map[y][x]
                moisture = moisture_map[y][x]
                has_mineral = mineral_map[y][x]

                # Determine terrain type based on multiple factors
                terrain_type = self._classify_terrain(elevation, moisture, has_mineral)
                row.append(terrain_type)
            terrain.append(row)

        return terrain

    def _generate_elevation_map(self, width, height):
        """Generate elevation using Perlin noise with seamless horizontal wrapping"""
        import math
        elevation_map = []
        scale = 100.0  # Lower = smoother terrain
        octaves = 5   # More = more detail

        # For seamless wrapping, map x coordinates onto a circle
        circumference = width / scale

        for y in range(height):
            row = []
            for x in range(width):
                # Map x onto a circle to make it wrap seamlessly
                angle = (x / width) * 2 * math.pi
                nx = math.cos(angle) * circumference / (2 * math.pi)
                ny_offset = math.sin(angle) * circumference / (2 * math.pi)

                # y is linear (no wrapping at poles for now)
                ny = y / scale

                # Base terrain - smooth continental features
                base_value = pnoise2(
                    nx + 100,
                    ny + ny_offset + 100,
                    octaves=octaves,
                    persistence=0.5,
                    lacunarity=2.0,
                    base=self.seed
                )

                # Add higher frequency detail for island chains
                detail_value = pnoise2(
                    nx * 3 + 200,
                    ny * 3 + ny_offset * 3 + 200,
                    octaves=3,
                    persistence=0.4,
                    lacunarity=2.5,
                    base=self.seed + 500
                )

                # Combine: base terrain + smaller detail features
                # Detail is scaled down so it adds peaks but doesn't dominate
                combined = base_value * 0.7 + detail_value * 0.3

                # Normalize to 0-1
                normalized = (combined + 1) / 2

                # Apply stronger contrast boost to create more distinct islands
                # This creates sharper boundaries between land and water
                contrast = 1.5
                adjusted = ((normalized - 0.5) * contrast) + 0.5
                adjusted = max(0, min(1, adjusted))  # Clamp to 0-1

                # Apply power curve to push more values to extremes
                # Creates tighter, more defined features
                adjusted = adjusted ** 0.85

                # Don't compress the range - use full 0-1 range
                # This ensures islands can form even on high water coverage planets
                row.append(adjusted)
            elevation_map.append(row)

        return elevation_map

    def _generate_moisture_map(self, width, height):
        """Generate moisture/water distribution with seamless horizontal wrapping"""
        import math
        moisture_map = []
        scale = 30.0  # Larger = bigger water bodies

        circumference = width / scale

        for y in range(height):
            row = []
            for x in range(width):
                # Map x onto a circle for seamless wrapping
                angle = (x / width) * 2 * math.pi
                nx = math.cos(angle) * circumference / (2 * math.pi)
                ny_offset = math.sin(angle) * circumference / (2 * math.pi)
                ny = y / scale

                value = pnoise2(
                    nx + 100,
                    ny + ny_offset + 100,
                    octaves=3,
                    persistence=0.5,
                    lacunarity=2.0,
                    base=self.seed + 1000  # Different seed for different pattern
                )

                # Normalize to 0-1
                normalized = (value + 1) / 2
                row.append(normalized)
            moisture_map.append(row)

        return moisture_map

    def _generate_mineral_map(self, width, height):
        """Generate mineral deposit locations with seamless horizontal wrapping"""
        import math
        mineral_map = []
        scale = 15.0  # Smaller = more scattered deposits

        circumference = width / scale

        for y in range(height):
            row = []
            for x in range(width):
                # Map x onto a circle for seamless wrapping
                angle = (x / width) * 2 * math.pi
                nx = math.cos(angle) * circumference / (2 * math.pi)
                ny_offset = math.sin(angle) * circumference / (2 * math.pi)
                ny = y / scale

                value = pnoise2(
                    nx + 100,
                    ny + ny_offset + 100,
                    octaves=2,
                    persistence=0.5,
                    lacunarity=2.0,
                    base=self.seed + 2000  # Different seed again
                )

                # Normalize to 0-1
                normalized = (value + 1) / 2

                # Mineral appears if value is high enough
                # mineral_richness controls threshold
                has_mineral = normalized > (1.0 - self.mineral_richness * 0.3)
                row.append(has_mineral)
            mineral_map.append(row)

        return mineral_map

    def _classify_terrain(self, elevation, moisture, has_mineral):
        """
        Classify terrain based on elevation, moisture, and minerals

        Args:
            elevation: 0-1, height above sea level
            moisture: 0-1, water content
            has_mineral: bool, whether minerals are present

        Returns:
            TerrainType constant
        """
        # Calculate water level based on planet's water coverage
        water_level = self.water_coverage

        # Deep water
        if elevation < water_level - 0.1:
            return TerrainType.DEEP_WATER

        # Shallow water
        if elevation < water_level:
            return TerrainType.SHALLOW_WATER

        # Check for minerals first (overrides other terrain)
        if has_mineral and elevation > water_level + 0.1:
            return TerrainType.MINERAL

        # Land terrain based on elevation and moisture
        if elevation < water_level + 0.02:
            # Very thin beach/coastal strip
            return TerrainType.SAND
        elif elevation < water_level + 0.15:
            # Low elevation land - moisture determines type
            if moisture > 0.3:
                return TerrainType.GRASS
            elif moisture > 0.25:
                return TerrainType.ROCK
            else:
                return TerrainType.SAND
        elif elevation < water_level + 0.35:
            # Medium elevation
            if moisture > 0.5:
                return TerrainType.GRASS
            else:
                return TerrainType.ROCK
        else:
            # High elevation (mountains)
            return TerrainType.MOUNTAIN

    def get_terrain_color(self, terrain_type):
        """
        Get RGB color for a terrain type

        Args:
            terrain_type: TerrainType constant

        Returns:
            RGB tuple
        """
        colors = {
            TerrainType.DEEP_WATER: (20, 50, 120),
            TerrainType.SHALLOW_WATER: (60, 100, 180),
            TerrainType.SAND: (210, 180, 140),
            TerrainType.GRASS: (80, 140, 60),
            TerrainType.ROCK: (100, 100, 100),
            TerrainType.MOUNTAIN: (150, 150, 150),
            TerrainType.MINERAL: (180, 140, 60),  # Gold/bronze color
        }
        return colors.get(terrain_type, (128, 128, 128))
