"""
Generic menu panel for displaying selectable menu options
Replaces BridgePanel, LandingControlPanel, and GasGiantWarningPanel
"""
import pygame
from ui.hud.hud_panel import HUDPanel
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class MenuConfig:
    """Configuration for a menu panel"""
    title: str
    items: List[str]
    title_color: Tuple[int, int, int] = (100, 200, 255)  # Default blue
    title_font: str = 'large'  # 'large' or 'default'
    warning_lines: Optional[List[str]] = None  # Optional warning text before items
    warning_color: Tuple[int, int, int] = (255, 200, 100)  # Default yellow
    danger_items: Optional[List[str]] = None  # Items that should be highlighted as dangerous (red)


class GenericMenuPanel(HUDPanel):
    """Generic menu panel - displays title, optional warning, and selectable items"""

    def __init__(self, x, y, width, height, config: MenuConfig):
        """
        Initialize generic menu panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width
            height: Panel height
            config: MenuConfig with title, items, and styling
        """
        super().__init__(x, y, width, height)
        self.config = config
        self.items = config.items
        self.selected_index = 0

    def set_items(self, items: List[str]):
        """Update menu items"""
        self.items = items
        # Clamp selected index to valid range
        if self.selected_index >= len(items):
            self.selected_index = max(0, len(items) - 1)

    def render_content(self, screen, renderer, game_state, coordinates=None):
        """
        Render menu without view data

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple (not used)
        """
        self._render_menu(screen, renderer, self.selected_index)

    def render_content_with_view_data(self, screen, renderer, game_state, coordinates, view_data):
        """
        Render menu with view data

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple
            view_data: Dictionary containing 'selected_index', etc.
        """
        # View data key can vary - try multiple common keys
        selected_index = view_data.get('selected_index',
                        view_data.get('selected_menu_index',
                        view_data.get('selected_landing_option',
                        view_data.get('selected_warning_option', 0))))
        self._render_menu(screen, renderer, selected_index)

    def render(self, screen, renderer):
        """Override to add title rendering in border"""
        # Draw panel background and border
        super().render(screen, renderer)

        # Draw title in border
        self.render_title(screen, renderer, self.config.title, self.config.title_color)

    def _render_menu(self, screen, renderer, selected_index):
        """
        Internal method to render the menu

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            selected_index: Index of selected item
        """
        content_x, content_y, content_width, content_height = self.get_content_rect()

        # Track Y offset for menu items (start at top of content area)
        y_offset = content_y + 5

        # Render warning lines if present
        if self.config.warning_lines:
            line_height = 20
            for line in self.config.warning_lines:
                renderer.draw_text(
                    line,
                    content_x + 10,
                    y_offset,
                    color=self.config.warning_color,
                    font=renderer.default_font
                )
                y_offset += line_height

            # Add spacing after warning
            y_offset += 20

        # Render menu items as boxes
        box_height = 30
        box_spacing = 5
        box_width = content_width - 20

        for i, item in enumerate(self.items):
            is_selected = (i == selected_index)
            is_danger = self.config.danger_items and item in self.config.danger_items

            # Draw box background
            box_rect = pygame.Rect(
                content_x + 10,
                y_offset,
                box_width,
                box_height
            )

            # Background fill - highlight if selected, red if danger
            if is_selected:
                if is_danger:
                    pygame.draw.rect(screen, (100, 40, 40), box_rect)  # Dark red
                else:
                    pygame.draw.rect(screen, (60, 80, 100), box_rect)  # Normal selection
            else:
                pygame.draw.rect(screen, (30, 30, 40), box_rect)

            # Border - brighter if selected, red if danger
            if is_selected:
                if is_danger:
                    pygame.draw.rect(screen, (255, 100, 100), box_rect, 2)  # Red border
                else:
                    pygame.draw.rect(screen, (150, 180, 200), box_rect, 2)  # Normal border
            else:
                pygame.draw.rect(screen, (80, 80, 100), box_rect, 1)

            # Draw item text centered vertically in box
            text_y = y_offset + (box_height - 16) // 2  # Center text vertically
            text_color = (255, 255, 255) if is_selected else (200, 200, 220)
            renderer.draw_text(
                item,
                content_x + 20,
                text_y,
                color=text_color,
                font=renderer.default_font
            )

            y_offset += box_height + box_spacing
