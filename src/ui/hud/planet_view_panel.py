"""
Planet view panel for orbit screen
Displays the planet being orbited
"""
import pygame
from ui.hud.hud_panel import HUDPanel
from core.terrain_generator import TerrainGenerator
from ui.planet_sphere_renderer import PlanetSphereRenderer


class PlanetViewPanel(HUDPanel):
    """Panel that displays the planet in orbit view"""

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.planet = None
        self.terrain_grid = None
        self.terrain_generator = None
        self.sphere_renderer = PlanetSphereRenderer(radius=150)

    def set_planet(self, planet):
        """Set the planet to display"""
        self.planet = planet

    def update(self, delta_time, game_state):
        """Update panel (get planet from game state)"""
        new_planet = game_state.orbiting_planet

        # If planet changed, generate new terrain
        if new_planet != self.planet:
            self.planet = new_planet
            self._generate_terrain()

        # Update sphere rotation
        if self.terrain_grid:
            self.sphere_renderer.update(delta_time)

    def render(self, screen, renderer):
        """Render the panel background"""
        # Draw panel background with space-like appearance
        pygame.draw.rect(screen, (10, 10, 20), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (50, 50, 100), (self.x, self.y, self.width, self.height), 2)

    def _generate_terrain(self):
        """Generate terrain for current planet"""
        if not self.planet:
            self.terrain_grid = None
            self.terrain_generator = None
            return

        # Generate terrain for all planets (200x100 for sphere mapping - optimized)
        # Gas giants and non-landable planets still get terrain, but landing is prevented elsewhere
        self.terrain_generator = TerrainGenerator(self.planet)
        self.terrain_grid = self.terrain_generator.generate(200, 100)

    def render_content(self, screen, renderer, game_state, **kwargs):
        """Render the planet view content"""
        # Check if we're in loading state
        loading = kwargs.get('loading', False)

        # Get planet from game_state
        planet = game_state.orbiting_planet

        if not planet:
            return

        # Show loading message if still generating terrain
        if loading:
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2

            renderer.draw_text_centered(
                f"Scanning {planet['name']}...",
                center_x,
                center_y - 20,
                color=(100, 200, 255),
                font=renderer.large_font
            )
            renderer.draw_text_centered(
                "Generating planetary data",
                center_x,
                center_y + 20,
                color=(150, 150, 150),
                font=renderer.default_font
            )
            return

        # Draw rotating planet sphere (all planets now have terrain)
        if not self.terrain_grid or not self.terrain_generator:
            return

        # Center of panel
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        # Render the sphere
        self.sphere_renderer.render_optimized(
            screen,
            center_x,
            center_y,
            self.terrain_grid,
            self.terrain_generator
        )

        # Draw planet name at top
        renderer.draw_text_centered(
            planet['name'],
            center_x,
            self.y + 20,
            color=(255, 255, 255),
            font=renderer.large_font
        )

    def _render_terrain(self, screen, renderer):
        """Render terrain grid"""
        # Calculate grid display area (below title)
        grid_start_y = self.y + 80
        grid_width = 400
        grid_height = 350
        grid_start_x = self.x + (self.width - grid_width) // 2

        # Calculate cell size
        cell_width = grid_width / 50
        cell_height = grid_height / 50

        # Draw terrain cells
        for y in range(50):
            for x in range(50):
                terrain_type = self.terrain_grid[y][x]
                color = self.terrain_generator.get_terrain_color(terrain_type)

                # Calculate cell position
                cell_x = grid_start_x + x * cell_width
                cell_y = grid_start_y + y * cell_height

                # Draw filled rectangle for this terrain cell
                pygame.draw.rect(
                    screen,
                    color,
                    (int(cell_x), int(cell_y), int(cell_width) + 1, int(cell_height) + 1)
                )

    def _render_planet_sphere(self, screen, renderer, planet):
        """Render planet as a sphere (for gas giants, etc.)"""
        # Calculate planet position (centered below title)
        planet_x = self.x + self.width // 2
        planet_y = self.y + 250
        planet_radius = 80

        # Draw the planet sphere
        pygame.draw.circle(
            screen,
            planet['color'],
            (planet_x, planet_y),
            planet_radius
        )

        # Draw "No surface" text
        renderer.draw_text_centered(
            "No landable surface",
            planet_x,
            planet_y + planet_radius + 30,
            color=(150, 150, 150)
        )
