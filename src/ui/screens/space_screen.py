"""
Space navigation screen
Handles movement in space, starfield rendering, and navigation
"""
import pygame
import random
from core.screen_manager import Screen


class SpaceScreen(Screen):
    """Space navigation screen with grid-based movement"""

    def __init__(self, screen_manager, game_state):
        super().__init__(screen_manager)
        self.game_state = game_state

        # Movement configuration
        self.ship_speed = 1.0  # Movement grid units per frame when key held
        self.fuel_consumption_rate = 0.01  # Fuel per movement grid unit traveled

        # Starfield for parallax effect
        self.stars = []
        self.generate_starfield()

    def generate_starfield(self):
        """Generate random stars for background"""
        self.stars = []
        for _ in range(200):  # 200 stars
            star = {
                'x': random.randint(0, 800),
                'y': random.randint(0, 600),
                'brightness': random.randint(100, 255),
                'size': random.choice([1, 1, 1, 2])  # Mostly small stars, some bigger
            }
            self.stars.append(star)

    def on_enter(self):
        """Called when entering space"""
        print("Entered space")
        # Regenerate starfield for variety
        self.generate_starfield()

    def update(self, delta_time, input_handler):
        """Update space screen"""
        # Return to starport
        if input_handler.is_key_just_pressed(pygame.K_r):
            if self.game_state.return_to_starport():
                print("Returning to starport")
                self.screen_manager.change_screen("starport")
                return

        # WASD movement
        dx = 0
        dy = 0

        if input_handler.is_up_pressed():  # W
            dy -= self.ship_speed
        if input_handler.is_down_pressed():  # S
            dy += self.ship_speed
        if input_handler.is_left_pressed():  # A
            dx -= self.ship_speed
        if input_handler.is_right_pressed():  # D
            dx += self.ship_speed

        # Apply movement if any
        if dx != 0 or dy != 0:
            # Store old position to calculate actual movement
            old_x = self.game_state.ship_x
            old_y = self.game_state.ship_y

            # Move the ship (may be clamped at boundaries)
            self.game_state.move_ship(int(dx), int(dy))

            # Calculate actual movement that occurred (after clamping)
            actual_dx = self.game_state.ship_x - old_x
            actual_dy = self.game_state.ship_y - old_y

            # Consume fuel based on actual distance traveled
            distance = (actual_dx**2 + actual_dy**2) ** 0.5
            fuel_used = distance * self.fuel_consumption_rate
            self.game_state.fuel = max(0, self.game_state.fuel - fuel_used)

            # Update starfield for parallax effect (stars drift opposite to movement)
            # Only scroll based on actual movement, not intended movement
            self.update_starfield(-actual_dx * 2, -actual_dy * 2)

    def update_starfield(self, dx, dy):
        """Move stars to create parallax effect"""
        for star in self.stars:
            star['x'] += dx
            star['y'] += dy

            # Wrap stars around screen edges
            if star['x'] < 0:
                star['x'] += 800
            elif star['x'] > 800:
                star['x'] -= 800

            if star['y'] < 0:
                star['y'] += 600
            elif star['y'] > 600:
                star['y'] -= 600

    def render(self, screen):
        """Render space screen"""
        from ui.renderer import Renderer
        renderer = Renderer(screen)
        width, height = screen.get_size()

        # Clear to black (space!)
        renderer.clear((0, 0, 0))

        # Draw starfield
        self.render_starfield(screen)

        # Draw ship at center of screen
        self.render_ship(renderer, width, height)

        # Draw HUD
        self.render_hud(renderer, width, height)

    def render_starfield(self, screen):
        """Render the starfield background"""
        for star in self.stars:
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            if star['size'] == 1:
                screen.set_at((int(star['x']), int(star['y'])), color)
            else:
                pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])

    def render_ship(self, renderer, width, height):
        """Render the player's ship at screen center"""
        ship_x = width // 2
        ship_y = height // 2

        # Simple triangle ship pointing up
        ship_color = (100, 200, 255)
        points = [
            (ship_x, ship_y - 10),      # Top point
            (ship_x - 8, ship_y + 10),  # Bottom left
            (ship_x + 8, ship_y + 10)   # Bottom right
        ]
        pygame.draw.polygon(renderer.screen, ship_color, points)

        # Outline
        pygame.draw.polygon(renderer.screen, (255, 255, 255), points, 1)

    def render_hud(self, renderer, width, height):
        """Render HUD with coordinates and status"""
        # Get coordinate position
        coord_x, coord_y = self.game_state.get_coordinate_position()

        # Top-left HUD panel
        hud_x = 10
        hud_y = 10
        line_height = 25

        # Coordinates (most important)
        renderer.draw_text(
            f"Coordinates: {coord_x}, {coord_y}",
            hud_x,
            hud_y,
            color=(255, 255, 100),
            font=renderer.default_font
        )

        # Fuel
        fuel_color = (255, 100, 100) if self.game_state.fuel < 20 else (200, 200, 200)
        renderer.draw_text(
            f"Fuel: {self.game_state.fuel:.1f}",
            hud_x,
            hud_y + line_height,
            color=fuel_color,
            font=renderer.small_font
        )

        # Credits
        renderer.draw_text(
            f"Credits: {self.game_state.credits}",
            hud_x,
            hud_y + line_height * 2,
            color=(200, 200, 200),
            font=renderer.small_font
        )

        # Cargo
        renderer.draw_text(
            f"Cargo: {self.game_state.cargo_used}/{self.game_state.cargo_capacity}",
            hud_x,
            hud_y + line_height * 3,
            color=(200, 200, 200),
            font=renderer.small_font
        )

        # Instructions at bottom
        renderer.draw_text_centered(
            "WASD: Move  |  R: Return to Starport",
            width // 2,
            height - 20,
            color=(150, 150, 150),
            font=renderer.small_font
        )
