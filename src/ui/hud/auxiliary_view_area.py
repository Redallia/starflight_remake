"""
Auxiliary View Area
Supplemental information and graphics - upper-right corner
"""
import pygame


class AuxiliaryViewArea:
    """Smart area that renders auxiliary view content based on game state"""

    def __init__(self, x, y, width, height):
        """
        Initialize Auxiliary View Area

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

        # Styling (matches HUDPanel styling)
        self.background_color = (0, 0, 20, 180)  # Semi-transparent dark blue
        self.border_color = (100, 150, 200)  # Light blue
        self.border_width = 2

        # Minimap configuration
        self.map_size = min(width, height) - 20  # Leave margin for border
        self.map_x = x + (width - self.map_size) // 2
        self.map_y = y + (height - self.map_size) // 2

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
        # Draw background and border
        self._draw_panel_background(screen)

        # Render state-specific content
        if game_state.location == "space":
            self._render_minimap(screen, renderer, game_state, **kwargs)
        elif game_state.location == "orbit":
            self._render_terrain_map(screen, renderer, game_state, **kwargs)
        # elif game_state.location == "hyperspace":
        #     self._render_ship_systems(screen, renderer, game_state, **kwargs)

    def _draw_panel_background(self, screen):
        """Draw panel background and border"""
        # Draw background
        pygame.draw.rect(
            screen,
            self.background_color,
            (self.x, self.y, self.width, self.height)
        )

        # Draw border
        pygame.draw.rect(
            screen,
            self.border_color,
            (self.x, self.y, self.width, self.height),
            self.border_width
        )

    def _render_minimap(self, screen, renderer, game_state, **kwargs):
        """
        Render minimap for space navigation

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            **kwargs: Additional rendering data
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

    def _render_terrain_map(self, screen, renderer, game_state, **kwargs):
        """
        Render terrain map for orbit view

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            **kwargs: Additional rendering data
        """
        # TODO: Implement terrain map rendering
        # This will display a heightmap/terrain preview of the planet surface
        pass
