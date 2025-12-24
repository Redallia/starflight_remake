"""
Simple menu renderer for Starflight Remake
"""
import pygame
from core.colors import (
    MENU_TEXT,
    MENU_SELECTED,
    MENU_DISABLED,
    MENU_TITLE
)


class MenuRenderer:
    """Renders a simple text-based menu with selection highlighting"""

    def __init__(self, font_size=36):
        """
        Initialize the menu renderer

        Args:
            font_size: Size of the menu font
        """
        self.font = pygame.font.Font(None, font_size)
        self.title_font = pygame.font.Font(None, font_size * 2)

        # Colors from centralized palette
        self.text_color = MENU_TEXT
        self.highlight_color = MENU_SELECTED
        self.disabled_color = MENU_DISABLED
        self.title_color = MENU_TITLE

    def render(self, surface, title, options, selected_index, disabled_indices=None):
        """
        Render a menu on the given surface

        Args:
            surface: Pygame surface to render on
            title: Title text to display at top
            options: List of menu option strings
            selected_index: Index of currently selected option
            disabled_indices: Set of indices that are disabled (grayed out)
        """
        if disabled_indices is None:
            disabled_indices = set()

        screen_width = surface.get_width()
        screen_height = surface.get_height()

        # Render title
        title_surface = self.title_font.render(title, True, self.title_color)
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        surface.blit(title_surface, title_rect)

        # Calculate menu positioning
        menu_start_y = screen_height // 2 - (len(options) * 30)

        # Render each menu option
        for i, option in enumerate(options):
            # Determine color based on state
            if i in disabled_indices:
                color = self.disabled_color
            elif i == selected_index:
                color = self.highlight_color
            else:
                color = self.text_color

            # Render the option text
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, menu_start_y + i * 60))
            surface.blit(text_surface, text_rect)
