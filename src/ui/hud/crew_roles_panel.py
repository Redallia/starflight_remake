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
        Render crew roles in individual boxes

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple (not used in this panel)
        """
        import pygame

        content_x, content_y, content_width, content_height = self.get_content_rect()

        # Calculate box dimensions
        box_height = 35
        box_spacing = 5
        box_width = content_width - 20  # Leave margins on sides

        y_offset = content_y + 5

        # Render each role in its own box
        for role in self.roles:
            # Draw box background
            box_rect = pygame.Rect(
                content_x + 10,
                y_offset,
                box_width,
                box_height
            )

            # Background fill
            pygame.draw.rect(screen, (30, 30, 40), box_rect)

            # Border
            pygame.draw.rect(screen, (80, 80, 100), box_rect, 1)

            # Draw role text centered vertically in box
            text_y = y_offset + (box_height - 16) // 2  # Center text vertically (assuming ~16px font height)
            renderer.draw_text(
                role,
                content_x + 20,
                text_y,
                color=(200, 200, 220),
                font=renderer.default_font
            )

            y_offset += box_height + box_spacing
