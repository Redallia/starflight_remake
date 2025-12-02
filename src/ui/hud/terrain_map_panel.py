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
        self.grid_width = 500  # Planet terrain width
        self.grid_height = 200  # Planet terrain height

    def set_planet(self, planet):
        """Set the planet and generate terrain"""
        if planet != self.planet:
            self.planet = planet
            self._generate_terrain()

    def _generate_terrain(self):
        """Generate terrain for current planet"""
        if not self.planet:
            self.terrain_grid = None
            self.terrain_generator = None
            return

        # Check if planet has a surface
        terrain_params = self.planet.get('terrain_params', {})
        has_surface = terrain_params.get('has_surface', True)

        if not has_surface:
            self.terrain_grid = None
            self.terrain_generator = None
            return

        # Generate terrain (500x200 grid - original game dimensions)
        self.terrain_generator = TerrainGenerator(self.planet)
        self.terrain_grid = self.terrain_generator.generate(self.grid_width, self.grid_height)

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
        """Render the terrain map"""
        if not self.terrain_grid or not self.terrain_generator:
            # No terrain to display
            renderer.draw_text_centered(
                "No surface data",
                self.x + self.width // 2,
                self.y + self.height // 2,
                color=(100, 100, 100)
            )
            return

        # Calculate how to fit 500x200 terrain into panel (300x200)
        # We'll scale down the terrain to fit
        scale_x = self.width / self.grid_width
        scale_y = self.height / self.grid_height

        # Draw terrain cells scaled to fit panel
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                terrain_type = self.terrain_grid[y][x]
                color = self.terrain_generator.get_terrain_color(terrain_type)

                # Calculate cell position and size
                cell_x = self.x + x * scale_x
                cell_y = self.y + y * scale_y

                # Draw filled rectangle for this terrain cell
                # Add 1 to width/height to avoid gaps
                pygame.draw.rect(
                    screen,
                    color,
                    (int(cell_x), int(cell_y), max(1, int(scale_x) + 1), max(1, int(scale_y) + 1))
                )
