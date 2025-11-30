"""
HUD Manager - coordinates all HUD panels
"""


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

        # Panels (set by screens)
        self.status_panel = None
        self.info_panel = None
        self.message_log_panel = None

        # Instructions text (bottom center, above message log)
        self.instructions_text = ""
        self.instructions_color = (150, 150, 150)

    def set_status_panel(self, panel):
        """Set the status panel (top-left)"""
        self.status_panel = panel

    def set_info_panel(self, panel):
        """Set the info panel (upper-right)"""
        self.info_panel = panel

    def set_message_log_panel(self, panel):
        """Set the message log panel (bottom)"""
        self.message_log_panel = panel

    def set_instructions(self, text, color=(150, 150, 150)):
        """
        Set instructions text (shown above message log)

        Args:
            text: Instructions text
            color: RGB color tuple
        """
        self.instructions_text = text
        self.instructions_color = color

    def update(self, delta_time, game_state):
        """
        Update all panels

        Args:
            delta_time: Time since last frame
            game_state: Current game state
        """
        if self.status_panel:
            self.status_panel.update(delta_time, game_state)
        if self.info_panel:
            self.info_panel.update(delta_time, game_state)
        if self.message_log_panel:
            self.message_log_panel.update(delta_time, game_state)

    def render(self, screen, renderer, game_state, coordinates=None):
        """
        Render all HUD panels

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional coordinates to display in status panel
        """
        # Render status panel (top-left)
        if self.status_panel:
            self.status_panel.render(screen, renderer)
            self.status_panel.render_content(screen, renderer, game_state, coordinates)

        # Render info panel (upper-right)
        if self.info_panel:
            self.info_panel.render(screen, renderer)
            self.info_panel.render_content(screen, renderer, game_state)

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
