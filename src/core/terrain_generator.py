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
        """Generate elevation using Perlin noise"""
        elevation_map = []
        scale = 20.0  # Lower = smoother terrain
        octaves = 4   # More = more detail

        for y in range(height):
            row = []
            for x in range(width):
                # Generate Perlin noise value (-1 to 1)
                value = pnoise2(
                    x / scale,
                    y / scale,
                    octaves=octaves,
                    persistence=0.5,
                    lacunarity=2.0,
                    base=self.seed
                )

                # Normalize to 0-1 and apply elevation scale
                normalized = (value + 1) / 2
                scaled = normalized * self.elevation_scale + (1 - self.elevation_scale) / 2
                row.append(scaled)
            elevation_map.append(row)

        return elevation_map

    def _generate_moisture_map(self, width, height):
        """Generate moisture/water distribution"""
        moisture_map = []
        scale = 30.0  # Larger = bigger water bodies

        for y in range(height):
            row = []
            for x in range(width):
                value = pnoise2(
                    x / scale,
                    y / scale,
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
        """Generate mineral deposit locations"""
        mineral_map = []
        scale = 15.0  # Smaller = more scattered deposits

        for y in range(height):
            row = []
            for x in range(width):
                value = pnoise2(
                    x / scale,
                    y / scale,
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
        if elevation < water_level + 0.05:
            # Beach/coastal
            return TerrainType.SAND
        elif elevation < water_level + 0.2:
            # Low elevation land
            if moisture > 0.5:
                return TerrainType.GRASS
            else:
                return TerrainType.SAND
        elif elevation < water_level + 0.4:
            # Medium elevation
            if moisture > 0.6:
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
