"""
HUD Manager - coordinates all HUD panels and areas
"""
import pygame
from ui.hud.message_log_area import MessageLogArea
from ui.hud.main_view_area import MainViewArea
from ui.hud.auxiliary_view_area import AuxiliaryViewArea
from ui.hud.control_panel_area import ControlPanelArea


class HUDManager:
    """Manages all HUD panels and areas"""

    def __init__(self, screen_width=800, screen_height=600):
        """
        Initialize HUD manager

        Args:
            screen_width: Screen width (default 800)
            screen_height: Screen height (default 600)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Area-based architecture (per HUD specification)
        # Main View Area (left side, large area) - state-driven
        self.main_view_area = MainViewArea(0, 0, 500, 450)

        # Auxiliary View Area (upper-right) - state-driven
        self.auxiliary_view_area = AuxiliaryViewArea(500, 0, 300, 200)

        # Control Panel Area (right side, middle) - state-driven
        self.control_panel_area = ControlPanelArea(500, 200, 300, 250)

        # Message Log Area (bottom, full width) - state-independent
        self.message_log_area = MessageLogArea(0, 450, 800, 150)

        # Canvas border
        self.border_color = (100, 150, 200)  # Light blue
        self.border_width = 2

    def update(self, delta_time, game_state):
        """
        Update all HUD areas

        Args:
            delta_time: Time since last frame
            game_state: Current game state
        """
        # Update all areas
        self.main_view_area.update(delta_time, game_state)
        self.auxiliary_view_area.update(delta_time, game_state)
        self.control_panel_area.update(delta_time, game_state)
        self.message_log_area.update(delta_time, game_state)

    def render(self, screen, renderer, game_state, coordinates=None, view_data=None):
        """
        Render all HUD areas

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional coordinates to display in status panel
            view_data: Optional data for areas (e.g., near_planet)
        """
        # Prepare kwargs for areas
        kwargs = view_data or {}
        if coordinates:
            kwargs['coordinates'] = coordinates

        # Render all four HUD areas in order
        # Main View Area (background, left side)
        self.main_view_area.render(screen, renderer, game_state, **kwargs)

        # Auxiliary View Area (upper-right)
        self.auxiliary_view_area.render(screen, renderer, game_state, **kwargs)

        # Control Panel Area (right side, middle)
        self.control_panel_area.render(screen, renderer, game_state, **kwargs)

        # Message Log Area (bottom, full width)
        self.message_log_area.render(screen, renderer, game_state)

        # Draw canvas border (outermost edge)
        pygame.draw.rect(
            screen,
            self.border_color,
            (0, 0, self.screen_width, self.screen_height),
            self.border_width
        )

    def add_message(self, text, color=(200, 200, 200)):
        """
        Add a message to the message log

        Args:
            text: Message text
            color: RGB color tuple
        """
        self.message_log_area.add_message(text, color)

    def clear_messages(self):
        """Clear all messages from the message log"""
        self.message_log_area.clear_messages()
