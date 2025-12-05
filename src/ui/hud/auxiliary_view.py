"""
Mini-map panel for space navigation
Shows planetary system overview
"""
import pygame
from ui.hud.info_panel import InfoPanel


class MiniMapPanel(InfoPanel):
    """Mini-map display for space navigation"""

    def __init__(self, x, y, width, height):
        """
        Initialize mini-map panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width (300)
            height: Panel height (200)
        """
        super().__init__(x, y, width, height)

        # Use the smaller dimension for the square map
        self.map_size = min(width, height) - 20  # Leave margin for border

        # Center the map in the panel
        self.map_x = x + (width - self.map_size) // 2
        self.map_y = y + (height - self.map_size) // 2

    def render_content(self, screen, renderer, game_state, **kwargs):
        """
        Render mini-map content

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            **kwargs: Additional optional arguments (ignored)
        """
        # Draw grid lines (every 10 coordinates)
        grid_color = (40, 40, 60)
        for i in range(0, 51, 10):
            # Vertical lines
            x = self.map_x + (i / 50) * self.map_size
            pygame.draw.line(
                screen,
                grid_color,
                (int(x), self.map_y),
                (int(x), self.map_y + self.map_size),
                1
            )
            # Horizontal lines
            y = self.map_y + (i / 50) * self.map_size
            pygame.draw.line(
                screen,
                grid_color,
                (self.map_x, int(y)),
                (self.map_x + self.map_size, int(y)),
                1
            )

        # Draw planets
        for planet in game_state.planets:
            # Convert coordinate to mini-map position
            planet_map_x = self.map_x + (planet['coord_x'] / 50) * self.map_size
            planet_map_y = self.map_y + (planet['coord_y'] / 50) * self.map_size

            # Scale radius to mini-map (smaller)
            planet_map_radius = max(3, int(planet['radius'] * 1.2))

            # Draw planet
            pygame.draw.circle(
                screen,
                planet['color'],
                (int(planet_map_x), int(planet_map_y)),
                planet_map_radius
            )

            # Draw outline
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (int(planet_map_x), int(planet_map_y)),
                planet_map_radius,
                1
            )

        # Draw ship position
        ship_coord = game_state.get_coordinate_position()
        ship_map_x = self.map_x + (ship_coord[0] / 50) * self.map_size
        ship_map_y = self.map_y + self.map_size - (ship_coord[1] / 50) * self.map_size

        # Draw ship as bright triangle
        ship_size = 4
        ship_points = [
            (ship_map_x, ship_map_y - ship_size),      # Top
            (ship_map_x - ship_size, ship_map_y + ship_size),  # Bottom left
            (ship_map_x + ship_size, ship_map_y + ship_size)   # Bottom right
        ]
        pygame.draw.polygon(
            screen,
            (255, 255, 0),  # Bright yellow
            ship_points
        )

        # Draw ship outline
        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            ship_points,
            1
        )
