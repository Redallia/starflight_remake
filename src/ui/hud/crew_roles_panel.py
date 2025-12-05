"""
Crew roles panel for displaying ship crew positions
Shows: Captain, Navigator, Engineer, Science, Communications, Medic
"""
from ui.hud.hud_panel import HUDPanel


class CrewRolesPanel(HUDPanel):
    """Crew roles display panel"""

    def __init__(self, x, y, width, height):
        """
        Initialize crew roles panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width
            height: Panel height
        """
        super().__init__(x, y, width, height)

        # Define the six crew roles
        self.roles = [
            "Captain",
            "Navigator",
            "Engineer",
            "Science",
            "Communications",
            "Medic"
        ]

        self.selected_role = None  # For future interaction

    def render_content(self, screen, renderer, game_state, coordinates=None):
        """
        Render crew roles list

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple (not used in this panel)
        """
        content_x, content_y, content_width, content_height = self.get_content_rect()
        line_height = 35

        y_offset = content_y + 10

        # Render each role
        for role in self.roles:
            renderer.draw_text(
                role,
                content_x + 10,
                y_offset,
                color=(200, 200, 200),
                font=renderer.default_font
            )
            y_offset += line_height
