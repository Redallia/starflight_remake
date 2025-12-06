"""
Terrain map panel for orbit screen
Displays full planetary surface map (500x200)
"""
import pygame
from ui.hud.hud_panel import HUDPanel
from core.terrain_generator import TerrainGenerator


class TerrainMapPanel(HUDPanel):
    """Panel that displays the full planetary terrain map"""

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.planet = None
        self.terrain_grid = None
        self.terrain_generator = None
        self.grid_width = 200  # Planet terrain width (reduced from 500)
        self.grid_height = 100  # Planet terrain height (reduced from 200)
        self.cached_surface = None  # Cached rendered terrain surface
        self.sensor_data = None  # Sensor scan data (Mass/Bio/Min)

    def set_planet(self, planet):
        """Set the planet and generate terrain"""
        if planet != self.planet:
            self.planet = planet
            self.sensor_data = None  # Clear sensor data when planet changes
            self._generate_terrain()

    def set_sensor_data(self, sensor_data):
        """Set sensor data from scan"""
        self.sensor_data = sensor_data

    def _generate_terrain(self):
        """Generate terrain for current planet and cache it as a surface"""
        if not self.planet:
            self.terrain_grid = None
            self.terrain_generator = None
            self.cached_surface = None
            return

        # Generate terrain for all planets (200x100 grid - optimized for performance)
        # Gas giants and non-landable planets still get terrain, but landing is prevented elsewhere
        self.terrain_generator = TerrainGenerator(self.planet)
        self.terrain_grid = self.terrain_generator.generate(self.grid_width, self.grid_height)

        # Pre-render terrain to a cached surface
        self._cache_terrain_surface()

    def _cache_terrain_surface(self):
        """Render terrain once to a cached surface"""
        # Create a surface the size of the panel
        self.cached_surface = pygame.Surface((self.width, self.height))

        # Calculate scaling
        scale_x = self.width / self.grid_width
        scale_y = self.height / self.grid_height

        # Draw all terrain cells to the cached surface
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                terrain_type = self.terrain_grid[y][x]
                color = self.terrain_generator.get_terrain_color(terrain_type)

                # Calculate cell position and size
                cell_x = x * scale_x
                cell_y = y * scale_y

                # Draw to cached surface
                pygame.draw.rect(
                    self.cached_surface,
                    color,
                    (int(cell_x), int(cell_y), max(1, int(scale_x) + 1), max(1, int(scale_y) + 1))
                )

    def update(self, delta_time, game_state):
        """Update panel"""
        # Set planet from game state if in orbit
        if game_state.location == "orbit":
            self.set_planet(game_state.orbiting_planet)
        else:
            self.set_planet(None)

    def render(self, screen, renderer):
        """Render the panel background"""
        # Draw panel background
        pygame.draw.rect(screen, (10, 10, 20), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (50, 50, 100), (self.x, self.y, self.width, self.height), 2)

    def render_content(self, screen, renderer, game_state, **kwargs):
        """Render the terrain map (using cached surface)"""
        # Check if we're in loading state
        loading = kwargs.get('loading', False)

        if loading or not self.cached_surface:
            # Show loading or no data message
            message = "Scanning..." if loading else "No surface data"
            color = (100, 200, 255) if loading else (100, 100, 100)

            renderer.draw_text_centered(
                message,
                self.x + self.width // 2,
                self.y + self.height // 2,
                color=color
            )
            return

        # Draw sensor data readouts if available
        if self.sensor_data:
            text_y = self.y + 10
            text_color = (200, 200, 200)

            # Mass (in scientific notation)
            mass_str = f"Mass: {self.sensor_data.mass:,.0f} tons"
            renderer.draw_text(mass_str, self.x + 10, text_y, color=text_color)
            text_y += 18

            # Bio density
            bio_str = f"Bio: {self.sensor_data.bio_density:.1f}%"
            renderer.draw_text(bio_str, self.x + 10, text_y, color=text_color)
            text_y += 18

            # Mineral density
            min_str = f"Min: {self.sensor_data.mineral_density:.1f}%"
            renderer.draw_text(min_str, self.x + 10, text_y, color=text_color)
            text_y += 25

            # Blit the cached terrain surface below the sensor data
            terrain_y_offset = text_y - self.y
            # Create a subsurface or adjust blit position
            screen.blit(self.cached_surface, (self.x, text_y),
                       (0, terrain_y_offset, self.width, self.height - terrain_y_offset))
        else:
            # No sensor data - show full terrain map
            screen.blit(self.cached_surface, (self.x, self.y))
