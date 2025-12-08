"""
HUD Manager - coordinates all HUD panels
"""
import pygame


class HUDManager:
    """Manages all HUD panels and their layout"""

    def __init__(self, screen_width=800, screen_height=600):
        """
        Initialize HUD manager

        Args:
            screen_width: Screen width (default 800)
            screen_height: Screen height (default 600)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # HUD overlay panels (set by screens)
        # Using Starflight terminology:
        # Main view panel (renders behind HUD elements)
        self.view_panel = None

        # - Control Panel (right side, middle)
        self.control_panel = None

         # - Auxiliary Panel (right side, top)
        self.auxiliary_panel = None

        # - Message Log (bottom)
        self.message_log_panel = None

        # Instructions text (bottom center, above message log)
        self.instructions_text = ""
        self.instructions_color = (150, 150, 150)

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
        Update all panels

        Args:
            delta_time: Time since last frame
            game_state: Current game state
        """
        if self.view_panel:
            self.view_panel.update(delta_time, game_state)
        if self.control_panel:
            self.control_panel.update(delta_time, game_state)
        if self.auxiliary_panel:
            self.auxiliary_panel.update(delta_time, game_state)
        if self.message_log_panel:
            self.message_log_panel.update(delta_time, game_state)

    def render(self, screen, renderer, game_state, coordinates=None, view_data=None):
        """
        Render all HUD panels

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional coordinates to display in status panel
            view_data: Optional data for view panel (e.g., near_planet)
        """
        # Render main view panel first (background)
        if self.view_panel:
            self.view_panel.render(screen, renderer)
            self.view_panel.render_content(screen, renderer, game_state, **(view_data or {}))

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

        # Render message log (bottom)
        if self.message_log_panel:
            self.message_log_panel.render(screen, renderer)
            self.message_log_panel.render_content(screen, renderer)

        # Render instructions (above message log if present, otherwise at very bottom)
        if self.instructions_text:
            if self.message_log_panel:
                # Position above message log
                y_pos = self.message_log_panel.y - 25
            else:
                # Position at bottom of screen
                y_pos = self.screen_height - 20

            renderer.draw_text_centered(
                self.instructions_text,
                self.screen_width // 2,
                y_pos,
                color=self.instructions_color,
                font=renderer.small_font
            )

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
        if self.message_log_panel:
            self.message_log_panel.add_message(text, color)

    def clear_messages(self):
        """Clear all messages from the message log"""
        if self.message_log_panel:
            self.message_log_panel.clear_messages()
