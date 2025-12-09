"""
Control Panel Area
Navigable text-based menus - right side, middle
"""
import pygame


class ControlPanelArea:
    """Smart area that renders control panel content based on game state"""

    def __init__(self, x, y, width, height):
        """
        Initialize Control Panel Area

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
            self._render_ship_status(screen, renderer, game_state, **kwargs)
        elif game_state.location == "orbit":
            self._render_ship_status(screen, renderer, game_state, **kwargs)
        # elif game_state.location == "hyperspace":
        #     self._render_bridge_panel(screen, renderer, game_state, **kwargs)

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

    def get_content_rect(self):
        """Get content area rectangle (inside border)"""
        padding = self.border_width + 5
        return (
            self.x + padding,
            self.y + padding,
            self.width - padding * 2,
            self.height - padding * 2
        )

    def _render_ship_status(self, screen, renderer, game_state, **kwargs):
        """
        Render ship status (fuel, credits, cargo, coordinates)

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            **kwargs: Additional rendering data (coordinates, etc.)
        """
        content_x, content_y, content_width, content_height = self.get_content_rect()
        line_height = 25

        y_offset = content_y

        # Coordinates (if provided - most important)
        coordinates = kwargs.get('coordinates')
        if coordinates is not None:
            coord_x, coord_y = coordinates
            renderer.draw_text(
                f"Coordinates: {coord_x}, {coord_y}",
                content_x,
                y_offset,
                color=(255, 255, 100),
                font=renderer.default_font
            )
            y_offset += line_height

        # Fuel
        fuel_color = (255, 100, 100) if game_state.fuel < 20 else (200, 200, 200)
        renderer.draw_text(
            f"Fuel: {game_state.fuel:.1f}",
            content_x,
            y_offset,
            color=fuel_color,
            font=renderer.small_font
        )
        y_offset += line_height

        # Credits
        renderer.draw_text(
            f"Credits: {game_state.credits}",
            content_x,
            y_offset,
            color=(200, 200, 200),
            font=renderer.small_font
        )
        y_offset += line_height

        # Cargo
        renderer.draw_text(
            f"Cargo: {game_state.cargo_used}/{game_state.cargo_capacity}",
            content_x,
            y_offset,
            color=(200, 200, 200),
            font=renderer.small_font
        )
