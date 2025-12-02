"""
Planet view panel for orbit screen
Displays the planet being orbited
"""
import pygame
from ui.hud.hud_panel import HUDPanel


class PlanetViewPanel(HUDPanel):
    """Panel that displays the planet in orbit view"""

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.planet = None

    def set_planet(self, planet):
        """Set the planet to display"""
        self.planet = planet

    def update(self, delta_time, game_state):
        """Update panel (get planet from game state)"""
        self.planet = game_state.orbiting_planet

    def render(self, screen, renderer):
        """Render the panel background"""
        # Draw panel background with space-like appearance
        pygame.draw.rect(screen, (10, 10, 20), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (50, 50, 100), (self.x, self.y, self.width, self.height), 2)

    def render_content(self, screen, renderer, game_state, **kwargs):
        """Render the planet view content"""
        # Get planet from game state
        planet = game_state.orbiting_planet

        if not planet:
            renderer.draw_text_centered(
                "No planet data",
                self.x + self.width // 2,
                self.y + self.height // 2,
                color=(150, 150, 150)
            )
            return

        # Calculate planet position (centered in panel)
        planet_x = self.x + self.width // 2
        planet_y = self.y + self.height // 2
        planet_radius = 80  # Large radius for orbit view

        # Draw the planet
        pygame.draw.circle(
            screen,
            planet['color'],
            (planet_x, planet_y),
            planet_radius
        )

        # Draw planet name above the planet
        renderer.draw_text_centered(
            planet['name'],
            planet_x,
            planet_y - planet_radius - 30,
            color=(255, 255, 255),
            font=renderer.large_font
        )

        # Draw planet type below the planet
        planet_type = planet['type'].replace('_', ' ').title()
        renderer.draw_text_centered(
            f"Type: {planet_type}",
            planet_x,
            planet_y + planet_radius + 20,
            color=(200, 200, 200)
        )
