"""
Base class for HUD panels
All HUD components inherit from this
"""
import pygame


class HUDPanel:
    """Base class for all HUD panels"""

    def __init__(self, x, y, width, height):
        """
        Initialize HUD panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width
            height: Panel height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Common styling
        self.background_color = (0, 0, 20, 180)  # Semi-transparent dark blue
        self.border_color = (100, 150, 200)  # Light blue
        self.border_width = 2

    def update(self, delta_time, game_state):
        """
        Update panel state

        Args:
            delta_time: Time since last frame
            game_state: Current game state
        """
        pass

    def render(self, screen, renderer):
        """
        Render the panel background and border

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance for drawing utilities
        """
        # Draw background
        pygame.draw.rect(
            screen,
            self.background_color,
            (self.x, self.y, self.width, self.height)
        )

        # Draw border
        pygame.draw.rect(
            screen,
            self.border_color,
            (self.x, self.y, self.width, self.height),
            self.border_width
        )

    def render_title(self, screen, renderer, title, title_color=(100, 200, 255)):
        """
        Render panel title in the top border

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            title: Title text to display
            title_color: RGB color tuple for title
        """
        if not title:
            return

        # Calculate title box position (centered in top border area)
        title_surface = renderer.default_font.render(title, True, title_color)
        title_width = title_surface.get_width() + 10
        title_height = 20
        title_x = self.x + (self.width - title_width) // 2
        title_y = self.y - 10

        # Draw title background box
        pygame.draw.rect(
            screen,
            (20, 20, 40),
            (title_x, title_y, title_width, title_height)
        )

        # Draw title border
        pygame.draw.rect(
            screen,
            self.border_color,
            (title_x, title_y, title_width, title_height),
            1
        )

        # Draw title text
        renderer.draw_text(
            title,
            title_x + 5,
            title_y + 2,
            color=title_color,
            font=renderer.default_font
        )

    def render_content(self, screen, renderer, *args, **kwargs):
        """
        Render panel-specific content
        Override this in subclasses

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance for drawing utilities
            *args, **kwargs: Panel-specific arguments
        """
        pass

    def get_content_rect(self):
        """
        Get the inner rectangle (excluding border)

        Returns:
            Tuple of (x, y, width, height) for content area
        """
        padding = self.border_width + 5
        return (
            self.x + padding,
            self.y + padding,
            self.width - padding * 2,
            self.height - padding * 2
        )
