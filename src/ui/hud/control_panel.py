"""
Control panel for displaying ship status (fuel, credits, cargo, coordinates)
Right side, middle section of screen
"""
from ui.hud.hud_panel import HUDPanel


class ControlPanel(HUDPanel):
    """Ship status control panel"""

    def __init__(self, x, y, width, height):
        """
        Initialize control panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width
            height: Panel height
        """
        super().__init__(x, y, width, height)

    def render_content(self, screen, renderer, game_state, coordinates=None):
        """
        Render ship status

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple to display
        """
        content_x, content_y, content_width, content_height = self.get_content_rect()
        line_height = 25

        y_offset = content_y

        # Coordinates (if provided - most important)
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
