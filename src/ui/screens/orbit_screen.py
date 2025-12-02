"""
Orbit screen
Handles planetary orbit interface
"""
import pygame
from core.screen_manager import Screen


class OrbitScreen(Screen):
    """Orbital interface screen"""

    def __init__(self, screen_manager, game_state):
        super().__init__(screen_manager)
        self.game_state = game_state

    def on_enter(self):
        """Called when entering orbit"""
        pass

    def update(self, delta_time, input_handler):
        """Update orbit screen"""
        # Exit orbit with SPACE key
        if input_handler.is_confirm_pressed():
            if self.game_state.exit_orbit():
                self.screen_manager.change_screen("space")
                return

    def render(self, screen):
        """Render orbit screen"""
        from ui.renderer import Renderer
        renderer = Renderer(screen)

        # Clear screen to black
        screen.fill((0, 0, 0))

        # Get the planet we're orbiting
        planet = self.game_state.orbiting_planet
        if not planet:
            # Shouldn't happen, but handle gracefully
            renderer.draw_text_centered("Error: No planet data", 400, 300)
            return

        # Draw the planet in the center-left area (where space view was)
        planet_display_x = 250
        planet_display_y = 225
        planet_display_radius = 80  # Much larger for orbit view

        # Draw planet
        pygame.draw.circle(
            screen,
            planet['color'],
            (planet_display_x, planet_display_y),
            planet_display_radius
        )

        # Draw planet name
        renderer.draw_text_centered(
            planet['name'],
            planet_display_x,
            planet_display_y - planet_display_radius - 30,
            color=(255, 255, 255),
            font=renderer.large_font
        )

        # Draw planet type
        planet_type = planet['type'].replace('_', ' ').title()
        renderer.draw_text_centered(
            f"Type: {planet_type}",
            planet_display_x,
            planet_display_y + planet_display_radius + 20,
            color=(200, 200, 200)
        )

        # Draw instructions at the bottom
        renderer.draw_text_centered(
            "Press SPACE to exit orbit",
            400,
            550,
            color=(255, 255, 0)
        )
