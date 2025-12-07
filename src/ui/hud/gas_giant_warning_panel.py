"""
Gas giant warning panel for planetary landing interface
Shows warning and binary choice: Proceed, Abort
"""
import pygame
from ui.hud.hud_panel import HUDPanel


class GasGiantWarningPanel(HUDPanel):
    """Gas giant warning panel - shows danger warning and Proceed/Abort options"""

    def __init__(self, x, y, width, height, planet_name):
        """
        Initialize gas giant warning panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width
            height: Panel height
            planet_name: Name of the gas giant
        """
        super().__init__(x, y, width, height)
        self.planet_name = planet_name

        # Warning options
        self.options = [
            "Proceed",
            "Abort"
        ]

        # Currently selected option
        self.selected_index = 1  # Default to "Abort" for safety

    def render_content(self, screen, renderer, game_state, coordinates=None):
        """
        Render warning message and options

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple (not used in this panel)
        """
        self._render_warning(screen, renderer, self.selected_index)

    def render_content_with_view_data(self, screen, renderer, game_state, coordinates, view_data):
        """
        Render warning message and options with view data

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple (not used in this panel)
            view_data: Dictionary containing 'selected_warning_option', etc.
        """
        selected_index = view_data.get('selected_warning_option', 1)
        self._render_warning(screen, renderer, selected_index)

    def _render_warning(self, screen, renderer, selected_index):
        """
        Internal method to render warning and options

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            selected_index: Index of selected option
        """
        content_x, content_y, content_width, content_height = self.get_content_rect()

        # Warning title
        title_y = content_y + 10
        renderer.draw_text(
            "WARNING",
            content_x + 10,
            title_y,
            color=(255, 100, 100),
            font=renderer.large_font
        )

        # Warning message
        message_y = content_y + 40
        line_height = 20

        warning_lines = [
            f"Attempting to land on {self.planet_name}",
            "is inadvisable.",
            "",
            "Gas giants have no solid surface.",
            "Ship destruction is likely."
        ]

        for i, line in enumerate(warning_lines):
            renderer.draw_text(
                line,
                content_x + 10,
                message_y + (i * line_height),
                color=(255, 200, 100),
                font=renderer.default_font
            )

        # Calculate box dimensions for options
        box_height = 35
        box_spacing = 10
        box_width = content_width - 20
        y_offset = message_y + (len(warning_lines) * line_height) + 20

        # Render each option in its own box
        for i, option in enumerate(self.options):
            is_selected = (i == selected_index)

            # Draw box background
            box_rect = pygame.Rect(
                content_x + 10,
                y_offset,
                box_width,
                box_height
            )

            # Background fill - highlight if selected
            if is_selected:
                # Proceed gets red highlight, Abort gets normal highlight
                if option == "Proceed":
                    pygame.draw.rect(screen, (100, 40, 40), box_rect)  # Dark red
                else:
                    pygame.draw.rect(screen, (60, 80, 100), box_rect)  # Normal
            else:
                pygame.draw.rect(screen, (30, 30, 40), box_rect)

            # Border - brighter if selected
            if is_selected:
                if option == "Proceed":
                    pygame.draw.rect(screen, (255, 100, 100), box_rect, 2)  # Red border
                else:
                    pygame.draw.rect(screen, (150, 180, 200), box_rect, 2)
            else:
                pygame.draw.rect(screen, (80, 80, 100), box_rect, 1)

            # Draw option text centered vertically in box
            text_y = y_offset + (box_height - 16) // 2  # Center text vertically
            text_color = (255, 255, 255) if is_selected else (200, 200, 220)
            renderer.draw_text(
                option,
                content_x + 20,
                text_y,
                color=text_color,
                font=renderer.default_font
            )

            y_offset += box_height + box_spacing
