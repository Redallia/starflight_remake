"""
Main View Area
Primary visual centerpiece for gameplay - left side, large area
"""
import pygame
import random


class MainViewArea:
    """Smart area that renders main view content based on game state"""

    def __init__(self, x, y, width, height):
        """
        Initialize Main View Area

        Args:
            x: X position on screen
            y: Y position on screen
            width: Area width
            height: Area height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Starfield for space view (persistent across renders)
        self.stars = []
        self._generate_starfield()

    def _generate_starfield(self):
        """Generate random stars for space background"""
        self.stars = []
        for _ in range(200):  # 200 stars
            star = {
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'brightness': random.randint(100, 255),
                'size': random.choice([1, 1, 1, 2])  # Mostly small stars, some bigger
            }
            self.stars.append(star)

    def regenerate_starfield(self):
        """Regenerate starfield (called on screen enter)"""
        self._generate_starfield()

    def update_starfield(self, dx, dy):
        """
        Move stars to create parallax effect

        Args:
            dx: X offset to apply
            dy: Y offset to apply
        """
        for star in self.stars:
            star['x'] += dx
            star['y'] += dy

            # Wrap stars around screen edges
            if star['x'] < 0:
                star['x'] += self.width
            elif star['x'] > self.width:
                star['x'] -= self.width

            if star['y'] < 0:
                star['y'] += self.height
            elif star['y'] > self.height:
                star['y'] -= self.height

    def update(self, delta_time, game_state):
        """
        Update area state

        Args:
            delta_time: Time since last frame
            game_state: Current game state
        """
        pass

    def render(self, screen, renderer, game_state, **kwargs):
        """
        Render content based on game state

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            **kwargs: Additional rendering data
        """
        if game_state.location == "space":
            self._render_space_view(screen, renderer, game_state, **kwargs)
        # elif game_state.location == "orbit":
        #     self._render_orbit_view(screen, renderer, game_state, **kwargs)
        else:
            # Default: black background
            screen.fill((0, 0, 0))

    def _render_space_view(self, screen, renderer, game_state, **kwargs):
        """
        Render space navigation view

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            **kwargs: Additional rendering data
        """
        # Fill with pure black (space!)
        screen.fill((0, 0, 0))

        # Render starfield
        self._render_starfield(screen)

        # Render planets
        self._render_planets(screen, renderer, game_state)

        # Render ship at center
        self._render_ship(screen, renderer)

    def _render_starfield(self, screen):
        """Render the starfield background"""
        for star in self.stars:
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            if star['size'] == 1:
                screen.set_at((int(star['x']), int(star['y'])), color)
            else:
                pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])

    def _render_ship(self, screen, renderer):
        """Render the player's ship at screen center"""
        ship_x = self.width // 2
        ship_y = self.height // 2

        # Simple triangle ship pointing up
        ship_color = (100, 200, 255)
        points = [
            (ship_x, ship_y - 10),      # Top point
            (ship_x - 8, ship_y + 10),  # Bottom left
            (ship_x + 8, ship_y + 10)   # Bottom right
        ]
        pygame.draw.polygon(screen, ship_color, points)

        # Outline
        pygame.draw.polygon(screen, (255, 255, 255), points, 1)

    def _render_planets(self, screen, renderer, game_state):
        """Render planets relative to ship position"""
        # Use movement grid for smooth rendering
        ship_x = game_state.ship_x
        ship_y = game_state.ship_y

        for planet in game_state.planets:
            # Convert planet coordinate position to movement grid
            planet_x = planet['coord_x'] * 10
            planet_y = planet['coord_y'] * 10

            # Calculate planet position relative to ship (camera centered on ship)
            # Use movement grid for smooth scrolling
            movement_dx = planet_x - ship_x
            movement_dy = planet_y - ship_y

            # Scale to screen space (2 pixels per movement unit = 20 pixels per coordinate unit)
            screen_x = self.width // 2 + movement_dx * 2
            screen_y = self.height // 2 + movement_dy * 2  # Positive Y = down on screen

            # Only draw if on screen (with margin)
            margin = 100
            if -margin < screen_x < self.width + margin and -margin < screen_y < self.height + margin:
                # Draw planet
                planet_radius = planet['radius'] * 20  # Scale radius to screen
                pygame.draw.circle(
                    screen,
                    planet['color'],
                    (int(screen_x), int(screen_y)),
                    int(planet_radius)
                )

                # Draw outline
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (int(screen_x), int(screen_y)),
                    int(planet_radius),
                    2
                )

                # Draw planet name
                renderer.draw_text_centered(
                    planet['name'],
                    int(screen_x),
                    int(screen_y - planet_radius - 15),
                    color=(200, 200, 200),
                    font=renderer.small_font
                )
