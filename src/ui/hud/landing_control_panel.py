"""
Landing control panel for planetary landing interface
Shows: Site Select, Descend, Abort
"""
import pygame
from ui.hud.hud_panel import HUDPanel


class LandingControlPanel(HUDPanel):
    """Landing control panel - shows landing options"""

    def __init__(self, x, y, width, height):
        """
        Initialize landing control panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width
            height: Panel height
        """
        super().__init__(x, y, width, height)

        # Landing options
        self.options = [
            "Site Select",
            "Descend",
            "Abort"
        ]

        # Currently selected option
        self.selected_index = 0

    def render_content(self, screen, renderer, game_state, coordinates=None):
        """
        Render landing options

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple (not used in this panel)
        """
        self._render_options(screen, renderer, self.selected_index)

    def render_content_with_view_data(self, screen, renderer, game_state, coordinates, view_data):
        """
        Render landing options with view data

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple (not used in this panel)
            view_data: Dictionary containing 'selected_landing_option', etc.
        """
        selected_index = view_data.get('selected_landing_option', 0)
        self._render_options(screen, renderer, selected_index)

    def _render_options(self, screen, renderer, selected_index):
        """
        Internal method to render landing options

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            selected_index: Index of selected option
        """
        content_x, content_y, content_width, content_height = self.get_content_rect()

        # Title
        title_y = content_y + 10
        renderer.draw_text(
            "Landing Interface",
            content_x + 10,
            title_y,
            color=(100, 200, 255),
            font=renderer.large_font
        )

        # Calculate box dimensions
        box_height = 35
        box_spacing = 10
        box_width = content_width - 20
        y_offset = content_y + 50  # Start below title

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
                pygame.draw.rect(screen, (60, 80, 100), box_rect)  # Brighter background
            else:
                pygame.draw.rect(screen, (30, 30, 40), box_rect)

            # Border - brighter if selected
            if is_selected:
                pygame.draw.rect(screen, (150, 180, 200), box_rect, 2)  # Thicker, brighter border
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
