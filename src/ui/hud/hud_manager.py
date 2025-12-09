"""
HUD Manager - coordinates all HUD panels and areas
"""
import pygame
from ui.hud.message_log_area import MessageLogArea
from ui.hud.main_view_area import MainViewArea


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

        # HUD overlay panels (set by screens) - TO BE MIGRATED TO AREAS
        # Using Starflight terminology:
        # Main view panel (renders behind HUD elements)
        self.view_panel = None

        # - Control Panel (right side, middle)
        self.control_panel = None

         # - Auxiliary Panel (right side, top)
        self.auxiliary_panel = None

        # - Message Log (bottom) - LEGACY, use message_log_area instead
        self.message_log_panel = None

        # NEW: Area-based architecture
        # Main View Area (left side, large area) - state-driven
        self.main_view_area = MainViewArea(0, 0, 500, 450)

        # Message Log Area (bottom, full width) - state-independent
        self.message_log_area = MessageLogArea(0, 450, 800, 150)

        # Canvas border
        self.border_color = (100, 150, 200)  # Light blue
        self.border_width = 2

    def set_view_panel(self, panel):
        """Set the main view panel (background)"""
        self.view_panel = panel

    def set_control_panel(self, panel):
        """Set the control panel (right side, middle)"""
        self.control_panel = panel

    def set_auxiliary_panel(self, panel):
        """Set the auxiliary panel (right side, top)"""
        self.auxiliary_panel = panel

    def set_message_log_panel(self, panel):
        """Set the message log panel (bottom)"""
        self.message_log_panel = panel

    def update(self, delta_time, game_state):
        """
        Update all panels and areas

        Args:
            delta_time: Time since last frame
            game_state: Current game state
        """
        # Update legacy panels
        if self.control_panel:
            self.control_panel.update(delta_time, game_state)
        if self.auxiliary_panel:
            self.auxiliary_panel.update(delta_time, game_state)

        # Update areas
        self.main_view_area.update(delta_time, game_state)
        self.message_log_area.update(delta_time, game_state)

    def render(self, screen, renderer, game_state, coordinates=None, view_data=None):
        """
        Render all HUD panels and areas

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional coordinates to display in status panel
            view_data: Optional data for view panel (e.g., near_planet)
        """
        # Render main view area first (background)
        self.main_view_area.render(screen, renderer, game_state, **(view_data or {}))

        # Render HUD overlay panels on top
        # Render control panel (right side, middle)
        if self.control_panel:
            self.control_panel.render(screen, renderer)
            # Pass view_data to control panel for additional context (e.g., selected_role_index)
            if view_data and hasattr(self.control_panel, 'render_content_with_view_data'):
                self.control_panel.render_content_with_view_data(screen, renderer, game_state, coordinates, view_data)
            else:
                self.control_panel.render_content(screen, renderer, game_state, coordinates)

        # Render auxiliary panel (right side, top)
        if self.auxiliary_panel:
            self.auxiliary_panel.render(screen, renderer)
            self.auxiliary_panel.render_content(screen, renderer, game_state, **(view_data or {}))

        # Render message log area (bottom)
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
